from django.conf.urls.static import static
from HelpDesk import settings
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authenticate.views import *
from .API.resourses import MyUserViewsets

router = DefaultRouter()
router.register(r'auth-api', MyUserViewsets)

urlpatterns = [
    path('register/', RegisterCreateView.as_view(), name='register_url'),
    path('login/', Login.as_view(), name='login_url'),
    path('logout/', LogoutView.as_view(), name='logout_url'),
    path('', include(router.urls)),
]
