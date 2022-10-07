from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User
from recipes.models import InCartRecipe


class SubscribeInline(admin.TabularInline):
    model = Subscribe
    fk_name = 'user'


class InCartRecipeInline(admin.TabularInline):
    model = InCartRecipe


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (
        SubscribeInline,
        InCartRecipeInline,
    )
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
