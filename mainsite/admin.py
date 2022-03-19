from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
class MyUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('is_police', 'is_repair', 'is_insurance', 'is_customer')}),
    )

admin.site.register(User, MyUserAdmin)
admin.site.register(Product)
admin.site.register(Insurance)
admin.site.register(Repair)
admin.site.register(Theft)