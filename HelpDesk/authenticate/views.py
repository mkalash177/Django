from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView
from django.http.response import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from authenticate.API.serializers import MyUserSerializer
from authenticate.forms import RegisterForm
from authenticate.models import MyUser


class RegisterCreateView(CreateView):
    model = MyUser
    template_name = "authenticate/register.html"
    form_class = RegisterForm
    success_url = "authenticate//login"

    def form_valid(self, form):
        self.object = form.save()
        Token.objects.create(user=self.object)
        return HttpResponseRedirect(self.get_success_url())


class Login(LoginView):
    template_name = 'authenticate/login.html'
    success_url = '/statement'


class Logout(LogoutView):
    http_method_names = ['get']
    template_name = '/'


