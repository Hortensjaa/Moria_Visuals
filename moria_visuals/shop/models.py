from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.contrib import admin

from .types_and_sizes import SIZES, TYPES


# class Customer(User):
#     pass


class Product(models.Model):
    name = models.CharField(max_length=50, default='Fajna rzecz')
    description = models.TextField(max_length=250, default='Fajne, kupujcie')
    price = models.IntegerField(default=200)
    photo = models.ImageField(blank=True)
    type = models.CharField(choices=TYPES, max_length=50, default=TYPES[0])

    def __str__(self):
        return self.name

    @admin.display(description='price', )
    def price_string(self):
        return str(self.price) + ' zł'

    @admin.display(description='S', )
    def available_s(self):
        products = self.available_sizes.filter(size='S').values('count')
        if len(products) > 0:
            return products[0]['count']
        return None

    @admin.display(description='M', )
    def available_m(self):
        products = self.available_sizes.filter(size='M').values('count')
        if len(products) > 0:
            return products[0]['count']
        return None

    @admin.display(description='L', )
    def available_l(self):
        products = self.available_sizes.filter(size='L').values('count')
        if len(products) > 0:
            return products[0]['count']
        return None

    @admin.display(description='U', )
    def available_u(self):
        products = self.available_sizes.filter(size='U').values('count')
        if len(products) > 0:
            return products[0]['count']
        return None


class ProductStore(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='available_sizes')
    size = models.CharField(choices=SIZES, max_length=10, default=SIZES[3])
    count = models.IntegerField(default=10)

    def __str__(self):
        return self.product.name + ': ' + self.size

    def is_available(self):
        return self.count != models.IntegerField(0)

    def add_to_cart(self):
        self.count -= models.IntegerField(1)


class CartItem(models.Model):
    product = models.ForeignKey(ProductStore, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)