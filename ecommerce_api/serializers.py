from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Product, Category, Cart
from users.serializers import CustomUserSerializer
from users.models import CustomUser

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
            queryset=Category.objects.all(),
            write_only=True,
            source='category',
    )
    
    seller = CustomUserSerializer(read_only=True)
  
    class Meta:
        model = Product
        fields = '__all__'
        
    
    def create(self,validated_data):
        #print(validated_data)
        category_id = validated_data.pop('category')
        seller = self.context['request'].user
        
        product = Product.objects.create(category=category_id,seller=seller,**validated_data)
        return product
    
    def update(self, instance, validated_data):
        #print(validated_data)
        category_id = validated_data.pop('category')
        instance.category = category_id

        return super().update(instance,validated_data)




class CartSerializer(ModelSerializer):

    products = ProductSerializer(many=True, read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

    def update(self,instance, validated_data):
        product = validated_data.pop('product_id')

        if product.id in [product.id for product in instance.products.all()]:
            instance.products.remove(product)
            instance.save()
            return instance

        instance.products.add(product)
        instance.save()
        return instance
    
    