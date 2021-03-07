from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(User, CustomUserAdmin)
