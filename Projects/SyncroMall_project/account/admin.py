from django.contrib import admin

# Register your models here.
from .models import Customer, Tag, Product, Order
admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Order)