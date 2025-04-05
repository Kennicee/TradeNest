from django.contrib import admin
from .models import Product, Order  # Now Order is correctly defined

admin.site.register(Product)
admin.site.register(Order)

