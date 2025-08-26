from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from smart_homes.account.models import CustomUserModel

@admin.register(CustomUserModel)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_superuser")
    list_filter = ("is_superuser",)
    ordering = ("username",)