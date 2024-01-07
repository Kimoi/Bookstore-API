from django.contrib import admin
from .models import Book, Shop, Order, OrderItem

admin.site.register(Book)
admin.site.register(Shop)
admin.site.register(Order)
admin.site.register(OrderItem)
