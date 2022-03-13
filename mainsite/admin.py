from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Insurance)
admin.site.register(Repair)
admin.site.register(Theft)