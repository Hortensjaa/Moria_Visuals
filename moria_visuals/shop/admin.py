from django.contrib import admin

from django.contrib import admin
from .models import *
# Register your models here.


class Store(admin.TabularInline):
    model = ProductStore
    extra = 0
    classes = ['collapse']


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Description', {'fields': ['description']}),
        ('Price', {'fields': ['price']}),
        ('Photo', {'fields': ['photo']}),
        ('Type', {'fields': ['type']}),
    ]
    inlines = [Store]
    list_display = ('name', 'price_string', 'available_s', 'available_m', 'available_l', 'available_u')
    list_filter = ['type']
    search_fields = ['name']


admin.site.register(Product, ProductAdmin)
