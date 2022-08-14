from urllib.parse import urlunparse

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, F
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from annoying.fields import AutoOneToOneField

from .types_and_sizes import SIZES, TYPES


class Product(models.Model):
    name = models.CharField(max_length=50, default='Fajna rzecz')
    description = models.TextField(max_length=250, default='Fajne, kupujcie')
    price = models.PositiveIntegerField(default=200)
    photo = models.ImageField(blank=True)
    type = models.CharField(choices=TYPES, max_length=50, default=TYPES[0])

    def __str__(self):
        return self.name

    # @property
    # def url(self):
    #     url = urlunparse(('http', '127.0.0.1:8000', 'details/', '', f'product={self.name}', ''))
    #     return url.replace(' ', '%20')

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
    count = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.product.name + ': ' + self.size

    def is_available(self):
        return self.count != models.IntegerField(0)

    def add_to_cart(self):
        self.count -= models.IntegerField(1)


class Customer(AbstractUser):
    username = models.CharField(max_length=30, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    last_purchase = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.first_name:
            return self.first_name
        return self.email

    @property
    def cart(self):
        cart = CartItem.objects.filter(customer=self)
        cart = cart.annotate(name=F('product__product__name')).values('name', 'count')
        return cart

    #     def confirm_order(self):
    #         pass


class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='products_in_cart')
    product = models.ForeignKey(ProductStore, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)


# class Cart(models.Model):
#     customer = AutoOneToOneField(Customer, on_delete=models.CASCADE)
#     items = models.ManyToManyField(CartItem, blank=True)
#
#     def confirm_order(self):
#         pass
