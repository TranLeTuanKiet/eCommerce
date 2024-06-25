from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, Group, Permission
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id']

ROLE_CHOICES = (
    ('ADMIN', 'admin'),
    ('STAFF', 'staff'),
    ('SELLER', 'seller'),
    ('BUYER', 'buyer'),
)
STATUS_ORDER_CHOICES = (
    ('PENDING', 'pending'),
    ('ONGOING', 'ongoing'),
    ('SUCCESS', 'success'),
    ('ONHOLD', 'onhold')
)
GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
)

class User(AbstractUser):
    avatar = CloudinaryField(null=True, folder="avatars/")
    birth = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    address = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='BUYER')

class Category(BaseModel):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

class Store(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField(null=True, folder="store_avatars/")
    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    inventory_quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    image = CloudinaryField(null=True, folder="product_img/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products_cate')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products_store', null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    def __str__(self):
        return self.name

class Order(BaseModel):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='order_buyer')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, related_name='order_store')
    status = models.CharField(max_length=100, choices=STATUS_ORDER_CHOICES, default=STATUS_ORDER_CHOICES[0][0])
    total_price = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    def __str__(self):
        return f"Order #{self.id} from {self.store.name}: total {self.total_price}"

    def calculate_total_price(self):
        return sum(item.total_price() for item in self.details.all())

    def save(self, *args, **kwargs):
        if self.total_price is None:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)


class OrderDetail(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True) #don gia * so luong

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def total_price(self):
        return self.quantity * self.price

    class Meta:
        unique_together = ('order', 'product')

# Signals to update order total price when OrderDetail is modified
@receiver(post_save, sender=OrderDetail)
@receiver(post_delete, sender=OrderDetail)
def update_order_total_price(sender, instance, **kwargs):
    order = instance.order
    order.total_price = order.calculate_total_price()
    order.save()

class Tag(BaseModel):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name

class StoreInteraction(BaseModel):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class StoreComment(StoreInteraction):
    content = models.CharField(max_length=255)
    parent = models.ForeignKey('StoreComment', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.store.name} - {self.buyer.first_name}"

class StoreRating(StoreInteraction):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return f"{self.store.name} - {self.buyer.first_name} - {self.rating}"
    def clean(self):
        if int(self.rating) < 1 or int(self.rating) > 5:
            raise ValidationError("Rating must be between 1 and 5.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    class Meta:
        unique_together = ('buyer', 'store')


class ProductInteraction(BaseModel):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class ProductComment(ProductInteraction):
    content = models.CharField(max_length=255)
    parent = models.ForeignKey('ProductComment', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.product.name} - {self.buyer.first_name}"

class ProductRating(ProductInteraction):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.product.name} - {self.buyer.first_name} - {self.rating}"

    class Meta:
        unique_together = ('buyer', 'product')

class Cart(models.Model):
    buyer = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Cart of {self.buyer.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"



