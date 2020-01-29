from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages

from shop.forms import *
from shop.models import *


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
        obj.buy(price=self.info_product.price, quantity=self.request.POST.get('quantity_by_product'),
                info_product=self.info_product)
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
    template_name = 'shop/product_create.html'
    form_class = PurchaseReturnsForm
    success_url = reverse_lazy('my_buy_product_url')

    # def post(self, request, *args, **kwargs):
    #     self.return_product = Purchase.objects.get(id=kwargs.get('returns_id'))
    #     return super().post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        order_item = Purchase.objects.get(id=self.kwargs['returns_id'])
        if not order_item.return_is_valid():
            messages.error(request, f"Sorry, it is too late to return the order item.")
            return redirect('my_buy_product_url')
        order_item.is_returned = 'It is reviewing by admin. Please wait.'
        return_request = ReturnProduct()
        return_request.return_product = order_item
        return_request.save()
        order_item.save()
        return redirect('my_buy_product_url')

    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.return_product = self.return_product
    #     obj.save()
    #     return HttpResponseRedirect(self.success_url)


class ReturnsList(ListView):
    model = ReturnProduct
    paginate_by = 5
    template_name = 'shop/my_purchase_returns.html'
    queryset = ReturnProduct.objects.all()
    context_object_name = 'returns_product'


class AcceptReturn(DeleteView):
    model = Purchase

    def post(self, request, *args, **kwargs):
        order_item = self.get_object()
        order_item.refund(order_item=order_item)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('returns_user_url')

    def delete(self, request, *args, **kwargs):
        return_product = self.get_object()
        return_product.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class RejectReturn(DeleteView):
    model = ReturnProduct

    def delete(self, request, *args, **kwargs):
        return_request = self.get_object()
        purchase_item = return_request.return_product
        purchase_item.request_time = 'Your previous return request was denied by admin.'
        purchase_item.save()
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('returns_user_url')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

# def dismiss(request, pk):
#     print(pk)
#     return HttpResponse(pk)
#
#
# def access(request, pk):
#     rp = ReturnProduct.objects.get(pk=pk)
#     re = Purchase.objects.get
#     print(rp)
#     print(re)
#     return HttpResponseRedirect('/returnsuser')
#
