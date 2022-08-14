from urllib.parse import urlunparse

from django.db.models import Value, Q, F, URLField, Case, When, IntegerField, Sum
from django.db.models.functions import Concat
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomerCreationForm


def url(name):
    url = urlunparse(('http', '127.0.0.1:8000', 'details/', '', f'product={name}', ''))
    return url.replace(' ', '%20')


class SignUpView(CreateView):
    form_class = CustomerCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class HomePageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/products_list.html'

    def get(self, request):
        products = Product.objects.values('name', 'price') \
            .alias(count_all=Sum('available_sizes__count')).filter(count_all__gt=0)
        for product in products:
            product['url'] = url(product['name'])
        return Response({'products': products})


class DetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/product_details.html'

    def get(self, request):
        product_name = request.GET.get('product')
        product = Product.objects.values('name', 'price', 'description').get(name=product_name)
        sizes = ProductStore.objects.values('size').filter(product__name=product_name)
        sizes = sizes.annotate(is_available=Case(When(count__gt=0, then=Value(1)),
                                                 default=Value(0), output_field=IntegerField()))
        return Response({'product': product, 'sizes': sizes})


class CartView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order/cart.html'

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user
            if customer.cart:
                cart = customer.cart.annotate(price=F('product__product__price'),
                                              sum_item=F('price')*F('count'))
                for product in cart:
                    product['url'] = url(product['name'])
                summary = cart.aggregate(sum=Sum('sum_item'), number_of_items=Sum('count'))
                return Response({'cart': cart, 'summary': summary})
            return Response('You have nothing in your cart (yet!)')
        return Response('Log in to add item to cart')
