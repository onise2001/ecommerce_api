from rest_framework.filters import BaseFilterBackend
from .models import Product



class MyProductsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(seller=request.user)
        return queryset



class ProductFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name')
        category = request.query_params.get('category')

        queryset = queryset.filter(status=Product.STATUS_CHOICES[1][0])

        if name:
            queryset = queryset.filter(name=name)
        
        if category:
            queryset = queryset.filter(category__id=category)
        
        
        return queryset