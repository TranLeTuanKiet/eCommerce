from django.db.models.functions import TruncDay
from ecommerce.models import *
from django.db.models import Count, Sum
def total_revenue_by_day(start_date, end_date):
    orders = Order.objects.filter(active=True, status='SUCCESS', created_date__range=[start_date, end_date])\
        .annotate(day=TruncDay('created_date')).values('day').annotate(total_revenue=Sum('total_price')).order_by('day')
    for item in orders:
        item['day'] = item['day'].isoformat()

    return orders

def top_10_stores_by_success_orders(start_date, end_date):
    orders = Order.objects.filter(active=True, status='SUCCESS', created_date__range=[start_date, end_date])
    top_stores = orders.values('store__name').annotate(total_success_orders=Count('id')).order_by('-total_success_orders')[:10]

    return top_stores

def count_products_by_category():
    # Tất cả category không chứa category con
    categories = Category.objects.annotate(num_child=Count('children')).filter(active=True, num_child=0)

    count_products_by_category = categories.values('name').annotate(total_product=Count('products_cate')).order_by('total_product')

    return count_products_by_category

def total_buyer():
    return User.objects.filter(is_active=True, role='BUYER').count()
def total_store():
    return Store.objects.filter(active=True).count()

def total_order_pending():
    return Order.objects.filter(active=True, status='PENDING').count()

def total_product():
    return Product.objects.filter(active=True).count()

def total_revenue():
    return Order.objects.filter(active=True, status='SUCCESS').aggregate(total=Sum('total_price'))['total']


