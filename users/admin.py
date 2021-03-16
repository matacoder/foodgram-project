from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):

    list_filter = ("first_name", "email",)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": ("following",),
        }),
    )


admin.site.register(User, CustomUserAdmin)
