from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import CreateView, ListView, UpdateView

from shop.forms import ProductCreateForm, ProductBuyForm
from shop.models import Product, Purchase


class RegisterCreateView(CreateView):
    template_name = "shop/register.html"
    form_class = UserCreationForm
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
    # model = Purchase
    form_class = ProductBuyForm
    template_name = 'shop/my_buy_product.html'
    success_url = '/'
    product = None

    def post(self, request, *args, **kwargs):
        self.product = Product.objects.get(id=kwargs.get('prod_id'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.customer = self.request.user
        obj.product = self.product
        obj.save()
        return super().form_valid(form)
    # def post(self, request, *args, **kwargs):
    #     self.shop_product = Product.objects.all()
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         order = form.save(commit=False)
    #         for item in self.shop_product:
    #             Purchase.objects.create(order=order,
    #                                     info_user=item['info_user'],
    #                                     info_product=item['info_product'],
    #                                     quantity_by_product=item['quantity_by_product']
    #                                     )
    #         return render(request, 'shop/my_buy_product.html',
    #                       {'form': form})
