from django.db import models
from django.contrib.auth.models import AbstractUser
#from ecommerce_api.models import Cart
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('User', 'user'),
        ('Admin', 'admin')
    )

    role = models.CharField(max_length=100, choices=ROLE_CHOICES,default=ROLE_CHOICES[0][0])
    cart = models.ForeignKey(to='ecommerce_api.Cart', on_delete=models.CASCADE, related_name='mycart')