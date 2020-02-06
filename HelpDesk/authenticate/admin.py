from django.contrib import admin

# Register your models here.
from authenticate.models import MyUser

admin.site.register(MyUser)