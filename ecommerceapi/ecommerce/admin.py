from django.contrib import admin
from django.utils.html import mark_safe
from django.urls import path
from ecommerce.models import User, Product, Category, Order, OrderDetail, Store, Tag, ProductComment, ProductRating, StoreComment, StoreRating, Cart, CartItem
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.template.response import TemplateResponse
from ecommerce import dao
import datetime
class CommerceAdminSite(admin.AdminSite):
    def get_urls(self):
        return [path('ecommerce-stats/', self.stats_view)] + super().get_urls()

    def stats_view(self, request):
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        else:
            today = datetime.datetime.today()
            start_date = today - datetime.timedelta(days=30)
            end_date = today

        top_10_stores_by_success_orders = dao.top_10_stores_by_success_orders(start_date, end_date)
        total_revenue_by_day = dao.total_revenue_by_day(start_date, end_date)
        total_buyer = dao.total_buyer()
        total_store = dao.total_store()
        total_order_pending = dao.total_order_pending()
        total_product = dao.total_product()
        total_revenue = dao.total_revenue()
        count_products_by_category = dao.count_products_by_category()

        return TemplateResponse(request, 'admin/stats.html',{
            "total_buyer": total_buyer,
            "total_store": total_store,
            "total_order_pending": total_order_pending,
            "total_product": total_product,
            "top_10_stores_by_success_orders": top_10_stores_by_success_orders,
            "total_revenue_by_day": total_revenue_by_day,
            "count_products_by_category": count_products_by_category,
            "total_revenue": total_revenue,
            'start_date': start_date_str,
            'end_date': end_date_str,
        })

class DetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1

class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Product
        fields = '__all__'
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'gender', 'role', 'is_active']
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['id', 'username']
    readonly_fields = ['my_avatar']

    def my_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="150" height="150" />')
        return "No Image"

class MyProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inventory_quantity', 'price', 'created_date', 'updated_date', 'active']
    search_fields = ['name', 'description']
    list_filter = ['id', 'created_date', 'name']
    form = ProductForm
    readonly_fields = ['my_image']

    def my_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return "No Image"

class MyCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_date', 'updated_date', 'active']
    search_fields = ['name']
    list_filter = ['id', 'created_date', 'name']
class MyStoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone_number', 'created_date', 'updated_date', 'owner', 'active']
    search_fields = ['name']
    list_filter = ['id', 'created_date', 'name']
    readonly_fields = ['my_image']

    def my_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return "No Image"

class MyTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_date', 'updated_date', 'active']
    search_fields = ['name']
    list_filter = ['id', 'created_date', 'name']

class MyStoreComment(admin.ModelAdmin):
    list_display = ['id', 'store', 'buyer', 'created_date', 'updated_date', 'active']
    search_fields = ['store', 'content', 'buyer']
    list_filter = ['id', 'store', 'buyer']
class MyStoreRating(admin.ModelAdmin):
    list_display = ['id', 'store', 'buyer', 'rating', 'created_date', 'updated_date', 'active']
    search_fields = ['store', 'rating', 'buyer']
    list_filter = ['id', 'store', 'buyer', 'rating']

class MyProductComment(admin.ModelAdmin):
    list_display = ['id', 'product', 'buyer', 'created_date', 'updated_date', 'active']
    search_fields = ['product', 'content', 'buyer']
    list_filter = ['id', 'product', 'buyer']
class MyProductRating(admin.ModelAdmin):
    list_display = ['id', 'product', 'buyer', 'rating', 'created_date', 'updated_date', 'active']
    search_fields = ['product', 'rating', 'buyer']
    list_filter = ['id', 'product', 'buyer', 'rating']

class MyOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'store', 'buyer', 'total_price', 'status', 'created_date', 'updated_date', 'active']
    search_fields = ['store', 'buyer']
    list_filter = ['id', 'store', 'buyer']
    inlines = [DetailInline]

class MyOrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']

admin_site = CommerceAdminSite(name='ecommerce')
# Register your models here.
admin_site.register(User, MyUserAdmin)
admin_site.register(Category, MyCategoryAdmin)
admin_site.register(Tag, MyTagAdmin)
admin_site.register(Store, MyStoreAdmin)
admin_site.register(StoreComment, MyStoreComment)
admin_site.register(StoreRating, MyStoreRating)
admin_site.register(Product, MyProductAdmin)
admin_site.register(ProductComment, MyProductComment)
admin_site.register(ProductRating, MyProductRating)
admin_site.register(Order, MyOrderAdmin)
admin_site.register(OrderDetail, MyOrderDetailAdmin)
admin_site.register(Cart)
admin_site.register(CartItem)
