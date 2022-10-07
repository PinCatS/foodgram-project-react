from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    FavoriteRecipe,
    InCartRecipe,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
    TagRecipe,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', 'id')


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe


class FavoriteRecipeInline(admin.TabularInline):
    model = FavoriteRecipe


class InCartRecipeInline(admin.TabularInline):
    model = InCartRecipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'color')
    search_fields = ('slug', 'name', 'id')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        TagRecipeInline,
        IngredientRecipeInline,
        FavoriteRecipeInline,
        InCartRecipeInline,
    )
    list_display = (
        'name',
        'author',
    )

    readonly_fields = ('favorites',)

    @admin.display(description=_('times marked as favorite'))
    def favorites(self, obj):
        return obj.favorited_by.all().count()

    list_filter = ('tags__slug',)

    search_fields = ('name', 'author', 'tags__slug', 'tags__name', 'id')
