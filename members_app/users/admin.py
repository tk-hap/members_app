from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(ModelAdmin):
    list_display = ["date_joined", "username", "email", "first_name", "last_name"]
    model = User


admin.site.register(User, UserAdmin)
