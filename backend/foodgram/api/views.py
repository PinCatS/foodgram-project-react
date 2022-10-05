from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeFilter
from .paginator import DynamicLimitPaginator
from .serializers import (
    IngredientSerializer,
    ReadOnlyRecipeSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.models import (
    FavoriteRecipe,
    InCartRecipe,
    Ingredient,
    Recipe,
    Tag,
)
from recipes.serializers import SimpleRecipeSerializer

User = get_user_model()


class TagReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = RecipeFilter
    pagination_class = DynamicLimitPaginator

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeSerializer
        elif self.action == 'favorite':
            return SimpleRecipeSerializer
        return ReadOnlyRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        FavoriteRecipe.objects.create(
            recipe=recipe,
            user=request.user,
        )
        serializer = self.get_serializer(recipe)
        return Response(serializer.data)

    @favorite.mapping.delete
    def unfavorite(self, request, pk=None):
        FavoriteRecipe.objects.filter(recipe=pk, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        serializer_class=None,
        filter_backends=None,
        pagination_class=None,
    )
    def download_shopping_cart(self, request):
        user = request.user
        recipes = user.cart_recipes
        recipes = [recipe.recipe.name for recipe in user.cart_recipes.all()]
        return Response(', '.join(recipes))

    @action(detail=True, methods=['post'])
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        InCartRecipe.objects.create(
            recipe=recipe,
            user=request.user,
        )
        serializer = self.get_serializer(recipe)
        return Response(serializer.data)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        InCartRecipe.objects.filter(recipe=pk, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
