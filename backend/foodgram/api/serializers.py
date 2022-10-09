from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe
from users.serializers import CustomUserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class ReadOnlyIngredientAmountSerializer(serializers.ModelSerializer):
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


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                _('Ingredient amount should be positive.')
            )
        return value


class ReadOnlyRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    ingredients = ReadOnlyIngredientAmountSerializer(
        many=True, read_only=True, source='ingredient_recipes'
    )
    tags = TagSerializer(many=True, read_only=True)

    is_favorited = serializers.BooleanField()
    is_in_shopping_cart = serializers.BooleanField()

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
    image = Base64ImageField()
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

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                _('Recipe should have at least one ingredient.')
            )

        ingredient_ids = set()
        for entry in value:
            ingredient_id = entry['ingredient']['id']
            if ingredient_id in ingredient_ids:
                raise serializers.ValidationError(
                    _('Duplicate ingredient with id %(ingredient_id)s')
                    % {'ingredient_id': ingredient_id}
                )
            ingredient_ids.add(ingredient_id)
        return value

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                _('Recipe cooking time should be greater than zero.')
            )
        return value

    def create_ingredient_recipe(self, ingredient_recipe, recipe):
        amount = ingredient_recipe['amount']
        current_ingredient = Ingredient.objects.get(
            pk=ingredient_recipe['ingredient']['id']
        )
        IngredientRecipe.objects.create(
            ingredient=current_ingredient,
            recipe=recipe,
            amount=amount,
        )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredient_recipes = validated_data.pop('ingredient_recipes')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            current_tag = Tag.objects.get(pk=tag.id)
            TagRecipe.objects.create(tag=current_tag, recipe=recipe)
        for ingredient_recipe_data in ingredient_recipes:
            self.create_ingredient_recipe(ingredient_recipe_data, recipe)

        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredient_recipes_data = None
        if 'ingredient_recipes' in validated_data:
            ingredient_recipes_data = validated_data.pop('ingredient_recipes')

        instance = super().update(instance, validated_data)

        IngredientRecipe.objects.filter(recipe=instance.id).delete()
        if ingredient_recipes_data:
            lst = []
            for ingredient_recipe_data in ingredient_recipes_data:
                self.create_ingredient_recipe(ingredient_recipe_data, instance)
                lst.append(ingredient_recipe_data['ingredient']['id'])
            instance.ingredients.set(lst)

            instance.save()
        return instance
