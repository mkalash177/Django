from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from authenticate.forms import RegisterForm
from authenticate.models import MyUser


class RegisterCreateView(CreateView):
    model = MyUser
    template_name = "authenticate/register.html"
    form_class = RegisterForm
    success_url = "/login"


class Login(LoginView):
    template_name = 'authenticate/login.html'
    success_url = '/statement'


class Logout(LogoutView):
    http_method_names = ['get']
    template_name = '/'
