import operator
from distutils.util import strtobool
from functools import reduce
from itertools import chain

import django_filters
from django.db import models
from rest_framework import filters

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


class IngredientSearchFilter(filters.SearchFilter):
    """Search ingredients by name via name query parameter.
    Search is case-insensitive. First, ingredients that start with terms are
    searched. Second ingredients that contain terms. The search results
    are listed in search order:
     - ingredients that start with terms are listed first
     - than ingredients that contain terms are listed
    """

    search_param = 'name'

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)

        if not search_terms:
            return queryset

        istartswith_conditions = []
        icontains_conditions = []
        for search_term in search_terms:
            istartswith_conditions.append(
                models.Q(name__istartswith=search_term)
            )
            icontains_conditions.append(models.Q(name__icontains=search_term))

        istartswith_queryset = queryset.filter(
            reduce(operator.or_, istartswith_conditions)
        )

        icontains_queryset = queryset.filter(
            reduce(operator.or_, icontains_conditions)
        )

        return chain(
            istartswith_queryset,
            icontains_queryset.difference(istartswith_queryset),
        )
