from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
    )
    list_filter = (
        'is_staff',
        'is_active',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')


# admin.site.register(User, UserAdmin)
