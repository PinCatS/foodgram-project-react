from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateResponse

from .filters import IngredientSearchFilter, RecipeFilter
from .paginator import DynamicLimitPaginator
from .serializers import (
    IngredientSerializer,
    ReadOnlyIngredientAmountSerializer,
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

    def get_queryset(self):
        user = self.request.user
        favorites = user.favorite_recipes.filter(recipe__id=OuterRef('id'))
        in_cart_recipes = user.cart_recipes.filter(recipe__id=OuterRef('id'))
        return (
            Recipe.objects.all()
            .annotate(is_favorited=Exists(favorites))
            .annotate(is_in_shopping_cart=Exists(in_cart_recipes))
        )

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeSerializer
        elif self.action in ('favorite', 'shopping_cart'):
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
        serializer = SimpleRecipeSerializer(recipe)
        return Response(serializer.data)

    @favorite.mapping.delete
    def unfavorite(self, request, pk=None):
        favorite = get_object_or_404(
            FavoriteRecipe, recipe__id=pk, user=request.user
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        serializer_class=None,
        filter_backends=None,
        pagination_class=None,
    )
    def download_shopping_cart(self, request):
        user = request.user

        recipes = []
        result = []
        for recipe_cart in user.cart_recipes.all():
            serializer = ReadOnlyIngredientAmountSerializer(
                recipe_cart.recipe.ingredient_recipes,
                many=True,
                read_only=True,
            )
            recipes.append(recipe_cart.recipe.name)

            summary = defaultdict(int)
            for ingredient in serializer.data:
                summary[
                    (ingredient['name'], ingredient['measurement_unit'])
                ] += ingredient['amount']

            for ingredient, amount in summary.items():
                name, measurement_unit = ingredient
                result.append(
                    {
                        'name': name,
                        'amount': amount,
                        'measurement_unit': measurement_unit,
                    }
                )

        template = 'template.html'
        context = {
            'recipes': recipes,
            'ingredients': result,
        }

        response = PDFTemplateResponse(
            request=request,
            template=template,
            filename="shopping_cart.pdf",
            context=context,
            show_content_in_browser=False,
            cmd_options={
                'margin-top': 50,
            },
        )
        return response

    @action(detail=True, methods=['post'])
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        InCartRecipe.objects.create(
            recipe=recipe,
            user=request.user,
        )
        serializer = SimpleRecipeSerializer(recipe)
        return Response(serializer.data)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        in_cart_recipe = get_object_or_404(
            InCartRecipe, recipe__id=pk, user=request.user
        )
        in_cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
