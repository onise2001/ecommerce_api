from django.db import models
from users.models import CustomUser
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100)


    # def __str__(self):
    #     return self.name


class Product(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'pending'),
        ('Approved', 'approved'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])




class Cart(models.Model):
    products = models.ManyToManyField(Product,blank=True, null=True, related_name='products')

