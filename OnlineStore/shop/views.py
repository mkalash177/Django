from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from shop.forms import ProductCreateForm, ProductBuyForm, RegisterForm, PurchaseReturnsForm
from shop.models import Product, Purchase, Person, ReturnProduct


class RegisterCreateView(CreateView):
    model = Person
    template_name = "shop/register.html"
    form_class = RegisterForm
    success_url = "/login"


class Login(LoginView):
    template_name = 'shop/login.html'


class Logout(LogoutView):
    template_name = '/'


class ProductListView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'shop/index.html'
    queryset = Product.objects.all()
    context_object_name = 'lists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'Buy': ProductBuyForm
        })
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    success_url = '/'
    template_name = 'shop/product_create.html'


class ProductChargeView(UpdateView):
    model = Product
    template_name = 'shop/charge_product.html'
    success_url = '/'
    fields = ['name', 'product_description', 'price', 'quantity_product']


class BuyProduct(CreateView):
    http_method_names = ['get', 'post']
    form_class = ProductBuyForm
    success_url = '/myproduct'
    info_product = None

    def post(self, request, *args, **kwargs):
        self.info_product = Product.objects.get(id=kwargs.get('product_id'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.info_user = self.request.user
        obj.info_product = self.info_product
        summ = int(self.request.POST.get('quantity_by_product')) * obj.info_product.price
        if obj.info_user.cash < int(summ):
            return HttpResponseRedirect('/myproduct')
        if int(self.request.POST.get('quantity_by_product')) > obj.info_product.quantity_product:
            return HttpResponseRedirect('/myproduct')
        obj.save()
        return HttpResponseRedirect('/myproduct')


class MyProduct(ListView):
    model = Product
    paginate_by = 100
    template_name = 'shop/my_buy_product.html'
    queryset = Purchase.objects.all()
    context_object_name = 'my_product'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Purchase.objects.filter(info_user_id=self.request.user.id)
            return queryset
        return super().get_queryset()



class PurchaseReturns(CreateView):
    http_method_names = ['get', 'post']
    template_name = 'shop/my_buy_product.html'
    form_class = PurchaseReturnsForm
    success_url = reverse_lazy('my_buy_product_ur')
    return_product = None

    def post(self, request, *args, **kwargs):
        self.return_products = ReturnProduct.objects.get(id=kwargs.get('returns_id'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.return_products = self.return_products
        obj.save()
        return HttpResponseRedirect(self.success_url)


class ReturnsList(ListView):
    model = ReturnProduct
    paginate_by = 5
    template_name = 'shop/my_purchase_returns.html'
    queryset = ReturnProduct.objects.all()
    context_object_name = 'returns_product'


