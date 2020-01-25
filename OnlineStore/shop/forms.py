from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from shop.models import Product, Purchase, Person


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_description', 'price', 'quantity_product']


class ProductBuyForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity_by_product']


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None