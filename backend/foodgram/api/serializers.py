import base64

from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True,
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class ReadOnlyRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    ingredients = IngredientAmountSerializer(
        many=True, read_only=True, source='ingredient_recipes'
    )
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'text',
            'is_favorited',
            'is_in_shopping_cart',
            'image',
            'cooking_time',
            'author',
            'tags',
            'ingredients',
        )


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    # Should be { "id": 1123, "amount": 10 }
    ingredients = IngredientAmountSerializer(
        many=True, source='ingredient_recipes'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'text',
            'image',
            'cooking_time',
            'tags',
            'ingredients',
        )
        read_only_fields = ('author',)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredient_recipes = validated_data.pop('ingredient_recipes')
        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)
            for tag in tags:
                current_tag = Tag.objects.get(pk=tag.id)
                TagRecipe.objects.create(tag=current_tag, recipe=recipe)
            for ingredient_recipe in ingredient_recipes:
                amount = ingredient_recipe['amount']
                current_ingredient = Ingredient.objects.get(
                    pk=ingredient_recipe['ingredient']['id']
                )
                IngredientRecipe.objects.create(
                    ingredient=current_ingredient, recipe=recipe, amount=amount
                )

        return recipe
