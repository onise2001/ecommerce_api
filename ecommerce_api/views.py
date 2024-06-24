from django.shortcuts import render
from .models import Product, Category, Cart
from .serializers import ProductSerializer, CategorySerializer, CartSerializer
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework import status
from .filters import ProductFilter, MyProductsFilter
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, SAFE_METHODS

# Create your views here.




class ProductViewSet(GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [ProductFilter]
    

    def list(self, request):
        queryset = self.filter_queryset(queryset=self.queryset)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        if instance:
           serializer = self.serializer_class(instance)
           return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
    

    def update(self,request, pk=None):
        instance = self.queryset.get(pk=pk)
        if instance:
            self.check_object_permissions(request=request,obj=instance)
            #request.data['category_id'] = request.data['category']['id']
            serializer = self.serializer_class(instance=instance, data={
                'name': request.data['name'],
                'description': request.data['description'],
                'price': request.data['price'],
                'seller': request.data['seller'],
                'category_id':request.data['category']['id'],
                'status': request.data['status'],
            })
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_404_NOT_FOUND)
        


    def create(self, request):
        
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request,pk=None):
        instance = self.queryset.get(pk=pk)
        
        if instance:
            self.check_object_permissions(request=request,obj=instance)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    def get_permissions(self):
        
        if self.action in ['list','option','head','retrieve']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        
        elif self.action == "create":
            permission_classes = [IsAuthenticated]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [CanUpdateProduct]

        elif self.action == 'destroy':
            permission_classes = [CanDeleteProduct]

        return [permission() for permission in permission_classes]

        




class CategoryViewSet(ViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]

    
    def list(self,request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self,request, pk=None):
        instance = self.queryset.get(pk=pk)
        if instance:
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    def destroy(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)



    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        if instance:
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_404_NOT_FOUND)
    





class CartViewSet(ViewSet):
    queryset = Product.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self,request):
        cart = request.user.cart
        serilaizer = self.serializer_class(cart)
        return Response(serilaizer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        
        serializer = self.serializer_class(instance=request.user.cart, data={'product_id':pk}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response(status=status.HTTP_404_NOT_FOUND)
    


class MyProductsView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [MyProductsFilter]
    permission_classes = [IsAuthenticated]
    



class AdminApproveProduct(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CanChangeProductStatus]
    lookup_field = 'pk'

    def update(self, request,*args, **kwargs):
        instance = self.get_object()
        instance.status = 'Approved'
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    