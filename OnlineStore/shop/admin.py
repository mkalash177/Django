from django.contrib import admin

from .models import *

admin.site.register(Person)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(ReturnProduct)
