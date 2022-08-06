from django.contrib import admin
from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomerCreationForm, CustomerChangeForm
from .models import Customer


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    list_display = ["email", "first_name", "last_name", "is_staff"]
    ordering = ("-is_staff", "last_name",)
    fieldsets = ((None, {"fields": ("username", "password")}),
                 ("Personal info", {"fields": ("first_name", "last_name", "email")}),
                 ("Important dates", {"fields": ("last_login", "date_joined", "last_purchase")}),
                 ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions",),
                                  "classes": ['collapse']}),)
    add_fieldsets = ((None, {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"), },),)


admin.site.register(Customer, CustomerAdmin)


class Store(admin.TabularInline):
    model = ProductStore
    extra = 0


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
