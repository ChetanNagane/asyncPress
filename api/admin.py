# api/admin.py

from django.contrib import admin
from .models import Request, Product

admin.site.register(Request)
admin.site.register(Product)
