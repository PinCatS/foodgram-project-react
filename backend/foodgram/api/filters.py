from distutils.util import strtobool

import django_filters

from recipes.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    BOOLEAN_CHOICES = (
        ('0', 'False'),
        ('1', 'True'),
    )

    is_favorited = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES, coerce=strtobool
    )
    is_in_shopping_cart = django_filters.TypedChoiceFilter(
        choices=BOOLEAN_CHOICES, coerce=strtobool
    )
    author = django_filters.NumberFilter(field_name='author__id')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        )
