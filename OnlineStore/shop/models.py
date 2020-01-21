from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Person(User):
    cash = models.PositiveIntegerField(default=10000)

    def __str__(self):
        return f"{self.username}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    product_description = models.TextField(max_length=150)
    price = models.PositiveIntegerField(null=False, default=0)
    quantity_product = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name, self.price, self.quantity_product}"


class Purchase(models.Model):
    info_user = models.OneToOneField(Person, on_delete=models.CASCADE)
    info_product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity_by_product = models.PositiveIntegerField(null=False, default=0)
    purchase_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.info_user, self.info_product}"


class ReturnProduct(models.Model):
    return_product = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.return_product}"
