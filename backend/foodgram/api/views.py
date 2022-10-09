from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Value
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateResponse

from .filters import IngredientSearchFilter, RecipeFilter
from .permissions import OwnerOrAdmin
from .serializers import (
    IngredientSerializer,
    ReadOnlyIngredientAmountSerializer,
    ReadOnlyRecipeSerializer,
    RecipeSerializer,
    TagSerializer,
)
from common.paginators import DynamicLimitPaginator
from common.serializers import SimpleRecipeSerializer
from common.utils import build_ingredients_summary, follow, unfollow
from recipes.models import (
    FavoriteRecipe,
    InCartRecipe,
    Ingredient,
    Recipe,
    Tag,
)

User = get_user_model()


class TagReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminUser,)


class IngredientReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    permission_classes = (IsAdminUser,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = RecipeFilter
    pagination_class = DynamicLimitPaginator

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = (OwnerOrAdmin,)
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        favorited, in_shopping_cart = Value(False), Value(False)
        if not user.is_anonymous:
            favorites = user.favorite_recipes.filter(recipe__id=OuterRef('id'))
            in_cart_recipes = user.cart_recipes.filter(
                recipe__id=OuterRef('id')
            )
            favorited = Exists(favorites)
            in_shopping_cart = Exists(in_cart_recipes)
        return (
            Recipe.objects.all()
            .annotate(is_favorited=favorited)
            .annotate(is_in_shopping_cart=in_shopping_cart)
        )

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeSerializer
        elif self.action in ('favorite', 'shopping_cart'):
            return SimpleRecipeSerializer
        return ReadOnlyRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, permission_classes=[OwnerOrAdmin])
    def download_shopping_cart(self, request):
        user = request.user

        recipes, ingredients = [], []

        if user.cart_recipes.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        for recipe_cart in user.cart_recipes.all():
            serializer = ReadOnlyIngredientAmountSerializer(
                recipe_cart.recipe.ingredient_recipes,
                many=True,
                read_only=True,
            )
            recipes.append(recipe_cart.recipe.name)
            ingredients.append(serializer.data)

        context = {
            'recipes': recipes,
            'ingredients': build_ingredients_summary(ingredients),
        }

        return PDFTemplateResponse(
            request=request,
            template='shopping_cart_template.html',
            filename='shopping_cart.pdf',
            context=context,
            show_content_in_browser=False,
            cmd_options={
                'margin-top': 16,
            },
        )

    @action(detail=True, methods=['post'])
    def shopping_cart(self, request, pk=None):
        return follow(self, request, pk, Recipe, 'recipe', InCartRecipe)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        return unfollow(request, pk, 'recipe', InCartRecipe)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        return follow(self, request, pk, Recipe, 'recipe', FavoriteRecipe)

    @favorite.mapping.delete
    def unfavorite(self, request, pk=None):
        return unfollow(request, pk, 'recipe', FavoriteRecipe)
