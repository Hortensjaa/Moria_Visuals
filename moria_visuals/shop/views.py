from urllib.parse import urlunparse

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Value, Q, F, URLField, Case, When, IntegerField, Sum
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView

from .forms import CustomerCreationForm


def make_url(product_id):
    url = urlunparse(('http', '127.0.0.1:8000', f'{product_id}/', '', '', ''))
    return url.replace(' ', '%20')


class SignUpView(CreateView):
    form_class = CustomerCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class HomePageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/products_list.html'

    def get(self, request):
        products = Product.objects.values('name', 'price', 'id') \
            .alias(count_all=Sum('available_sizes__count')).filter(count_all__gt=0)
        for product in products:
            product['url'] = make_url(product['id'])
        return Response({'products': products})


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_details.html', {'product': product, 'sizes': product.available_sizes.all})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    selected_size = product.available_sizes.get(pk=request.POST['size'])
    selected_size.count -= 1
    selected_size.save()

    if request.user.is_authenticated:
        customer = request.user
        product_in_cart = CartItem.objects.select_related().filter(customer=customer, product=selected_size)
        if product_in_cart:
            product_in_cart[0].count += 1
            product_in_cart[0].save()
        else:
            CartItem.objects.create(customer=customer, product=selected_size, count=1)

    return HttpResponseRedirect(reverse('cart'))


# class DetailView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'products/product_details.html'
#
#     def get(self, request):
#         product_name = request.GET.get('product')
#         product = Product.objects.values('name', 'price', 'description').get(name=product_name)
#         sizes = ProductStore.objects.values('size').filter(product__name=product_name)
#         sizes = sizes.annotate(is_available=Case(When(count__gt=0, then=Value(1)),
#                                                  default=Value(0), output_field=IntegerField()))
#         return Response({'product': product, 'sizes': sizes})
    #
    # def add_to_cart(self, request, product_id):
    #     product = get_object_or_404(Product, pk=product_id)
    #     selected_choice = product.available_sizes.get(size=request.POST['size'])
    #     return HttpResponseRedirect(reverse('Home page'))


class CartView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order/cart.html'

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user
            if customer.cart:
                cart = customer.cart.annotate(id=F('product__product__id'),
                                              size=F('product__size'),
                                              price=F('product__product__price'),
                                              sum_item=F('price')*F('count'))
                for product in cart:
                    product['url'] = make_url(product['id'])
                summary = cart.aggregate(sum=Sum('sum_item'), number_of_items=Sum('count'))
                return Response({'cart': cart, 'summary': summary})
            return Response({'text': 'You have nothing in your cart (yet!)'})
        return Response({'text': 'Log in to add item to cart'})
