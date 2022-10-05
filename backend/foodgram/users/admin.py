from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User


class SubscribeInline(admin.TabularInline):
    model = Subscribe
    fk_name = 'user'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (SubscribeInline,)
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
