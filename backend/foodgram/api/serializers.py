import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import transaction
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


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            image_format, img_str = data.split(';base64,')
            ext = image_format.split('/')[-1]
            data = ContentFile(base64.b64decode(img_str), name='temp.' + ext)

        return super().to_internal_value(data)


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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            lst = [tag.id for tag in tags_data]
            instance.tags.set(lst)
        with transaction.atomic():
            IngredientRecipe.objects.filter(recipe=instance.id).delete()
            if 'ingredient_recipes' in validated_data:
                ingredient_recipes_data = validated_data.pop(
                    'ingredient_recipes'
                )
                lst = []
                for ingredient_recipe in ingredient_recipes_data:
                    amount = ingredient_recipe['amount']
                    current_ingredient = Ingredient.objects.get(
                        pk=ingredient_recipe['ingredient']['id']
                    )
                    IngredientRecipe.objects.create(
                        ingredient=current_ingredient,
                        recipe=instance,
                        amount=amount,
                    )
                    lst.append(ingredient_recipe['ingredient']['id'])
                instance.ingredients.set(lst)

            instance.save()
        return instance
