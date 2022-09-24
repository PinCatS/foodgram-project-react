from django.contrib import admin

from .models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', 'id')


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'color')
    search_fields = ('slug', 'name', 'id')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        TagRecipeInline,
        IngredientRecipeInline,
    )
    list_display = (
        'name',
        'text',
        'is_favorited',
        'is_in_shopping_cart',
        'image',
        'author',
        'cooking_time',
    )

    list_filter = ('is_favorited', 'is_in_shopping_cart')

    search_fields = ('name', 'author', 'id')
