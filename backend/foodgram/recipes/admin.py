from django.contrib import admin
from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _

from .models import (
    FavoriteRecipe,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
    TagRecipe,
)


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe


class FavoriteRecipeInline(admin.TabularInline):
    model = FavoriteRecipe


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', 'id')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagForm
    list_display = ('slug', 'name', 'color')
    search_fields = ('slug', 'name', 'id')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        TagRecipeInline,
        IngredientRecipeInline,
        FavoriteRecipeInline,
    )
    list_display = (
        'name',
        'author',
    )
    readonly_fields = ('favorites',)
    list_filter = ('tags__slug',)
    search_fields = ('name', 'author', 'tags__slug', 'tags__name', 'id')

    @admin.display(description=_('times marked as favorite'))
    def favorites(self, obj):
        return obj.favorited_by.count()
