from . import views
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
    path('myproduct/', MyProduct.as_view(), name='my_buy_product_url'),
    path('returns/<int:returns_id>', PurchaseReturns.as_view(), name='my_purchase_returns'),
    path('returnsuser/', ReturnsList.as_view(), name='returns_user_url'),
    # path('returnsuser/accept/<int:pk>', AcceptReturn.as_view(), name='accept'),
    # path('returnsuser/reject/<int:pk>', RejectReturn.as_view(), name='reject')
    path('returnsuser/reject/<int:pk>', RejectReturn.as_view(),  name='reject_return'),
    path('returnsuser/accept/<int:pk>', AcceptReturn.as_view(),  name='access_return'),
]
