from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter(trailing_slash=False)
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'my_cart', CartViewSet, basename='mycart')

urlpatterns = [
    path('', include(router.urls)),
    path('my_products/', MyProductsView.as_view()),
    path('approve_product/<int:pk>', AdminApproveProduct.as_view()),
    

]
