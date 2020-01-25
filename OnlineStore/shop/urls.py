from django.urls import path, include

from shop.views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_url'),
    path('change/<int:pk>', ProductChargeView.as_view(), name='charge_product_url'),
    path('buyproduct/<int:product_id>', BuyProduct.as_view(), name='buy_product_url'),
    path('register/', RegisterCreateView.as_view(), name='register_url'),
    path('login/', Login.as_view(), name='login_url'),
    path('logout/', LogoutView.as_view(), name='logout_url'),
    path('product_create/', ProductCreateView.as_view(), name='product_create_url'),
    path('myproduct/', MyProduct.as_view(), name='my_buy_product_url')
]
