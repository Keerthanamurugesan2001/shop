from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    productname = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=2)
    productimage = models.ImageField(upload_to="images/", blank=True, null=True)
    checkbutton = models.BooleanField(default=False, null=True, blank=True)

    @staticmethod
    def get_all_products():
        return Product.objects.all()


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=False)

    @staticmethod
    def get_all_cart():
        return Cart.objects.all()
