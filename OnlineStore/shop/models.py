from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta, datetime
import pytz

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
    image = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return f"{self.name, self.price, self.quantity_product}"


class Purchase(models.Model):
    info_user = models.ForeignKey(Person, on_delete=models.CASCADE)
    info_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_by_product = models.PositiveIntegerField(null=False, default=1)
    purchase_time = models.DateTimeField(auto_now_add=True)
    is_returned = models.CharField(max_length=100, default='')

    def return_is_valid(self):
        created_time = self.purchase_time
        return_valid_time = created_time + timedelta(minutes=3)
        if datetime.now(tz=pytz.UTC) <= return_valid_time:
            return True
        return False

    def get_cost(self):
        return self.info_product.price * self.quantity_by_product

    def buy(self, price, quantity, info_product):
        self.info_user.cash -= price * int(quantity)
        self.info_user.save()
        info_product.quantity_product -= int(quantity)
        info_product.save()

    def refund(self, order_item):
        self.info_user.cash += order_item.info_product.price * order_item.quantity_by_product
        self.info_user.save()
        info_product = order_item.info_product
        info_product.quantity_product += order_item.quantity_by_product
        info_product.save()



    def __str__(self):
        return f"{self.info_user, self.info_product}"


class ReturnProduct(models.Model):
    return_product = models.OneToOneField(Purchase, on_delete=models.CASCADE,related_name='returns')
    request_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['request_time']

    def __str__(self):
        return f"{self.return_product}"
