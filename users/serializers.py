from rest_framework.serializers import ModelSerializer
from .models import CustomUser
from ecommerce_api.models import Cart

class CustomUserSerializer(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'cart', 'role']
        extra_kwargs = {'password': {'write_only': True}, 'cart':{'read_only': True}}

    
    def create(self,validated_data):
        password = validated_data.pop('password')
        cart = Cart.objects.create()
        user = CustomUser(**validated_data)
        user.cart = cart
        user.set_password(password)

        user.save()
        return user
