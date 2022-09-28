from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import RecipeFilter
from .paginator import DynamicLimitPaginator
from .serializers import (
    IngredientSerializer,
    ReadOnlyRecipeSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.models import Ingredient, Recipe, Tag


class TagReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = DynamicLimitPaginator

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeSerializer
        return ReadOnlyRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
