from django.conf.urls.static import static
from HelpDesk import settings
from . import views
from django.urls import path, include

from authenticate.views import *

urlpatterns = [
    path('register/', RegisterCreateView.as_view(), name='register_url'),
    path('login/', Login.as_view(), name='login_url'),
    path('logout/', LogoutView.as_view(), name='logout_url'),
]
