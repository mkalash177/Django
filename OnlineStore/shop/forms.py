from django.forms import ModelForm

from shop.models import Product, Purchase


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_description', 'price', 'quantity_product']


class ProductBuyForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity_by_product']
