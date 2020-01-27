

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# User = get_user_model()
# Create your models here.
from django.utils import timezone


class Person(AbstractUser):
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
    info_user = models.ForeignKey(Person, on_delete=models.CASCADE)
    info_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_by_product = models.PositiveIntegerField(null=False, default=0)
    purchase_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.info_user, self.info_product}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.info_product.quantity_product -= self.quantity_by_product
        self.info_product.save()
        return super().save(force_insert, force_update, using,
             update_fields)


class ReturnProduct(models.Model):
    return_product = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    request_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['request_time']

    def __str__(self):
        return f"{self.return_product}"
