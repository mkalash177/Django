from django.contrib import admin

# Register your models here.
from application_system.models import *

admin.site.register(Statement)
admin.site.register(Decision)
