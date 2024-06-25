from rest_framework import pagination

class ProductPaginator(pagination.PageNumberPagination):
    page_size = 10

class ReviewPaginator(pagination.PageNumberPagination):
    page_size = 10

class OrderPaginator(pagination.PageNumberPagination):
    page_size = 10