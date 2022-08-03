from urllib.parse import urlunparse

from django.db.models import Value, Q, F, URLField, Case, When, IntegerField, Sum
from django.db.models.functions import Concat
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *


class HomePageView(APIView):

    def get(self, request):
        rows = Product.objects.values('name', 'price')\
            .alias(count_all=Sum('available_sizes__count')).filter(count_all__gt=0)
        rows = rows.annotate(url=Concat(Value(urlunparse(('http', '127.0.0.1:8000',
                                                          'moria_visuals/details/', '', f'product=', ''))),
                                        'name', output_field=URLField()))
        return Response({'Nasze produkty': rows})


class DetailView(APIView):

    def get(self, request):
        product_name = request.GET.get('product')
        product = Product.objects.values('name', 'price', 'description').get(name=product_name)
        sizes = ProductStore.objects.values('size').filter(product__name=product_name)
        sizes = sizes.annotate(is_available=Case(When(count__gt=0, then=Value(1)),
                                                 default=Value(0), output_field=IntegerField()))
        return Response({'Informacje': product, 'Dostępne rozmiary': sizes})