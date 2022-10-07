# Generated by Django 4.1.1 on 2022-10-07 16:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FavoriteRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
            ],
            options={
                "verbose_name": "favorite recipe",
                "verbose_name_plural": "favorite recipes",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="InCartRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
            ],
            options={
                "verbose_name": "recipe in cart",
                "verbose_name_plural": "recipes in cart",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                ("name", models.CharField(max_length=256, verbose_name="name")),
                (
                    "measurement_unit",
                    models.CharField(max_length=256, verbose_name="measurement unit"),
                ),
            ],
            options={
                "verbose_name": "ingredient",
                "verbose_name_plural": "ingredients",
            },
        ),
        migrations.CreateModel(
            name="IngredientRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="amount",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredient_recipes",
                        to="recipes.ingredient",
                    ),
                ),
            ],
            options={
                "verbose_name": "recipe's ingredient",
                "verbose_name_plural": "recipe's ingredients",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                ("name", models.CharField(max_length=200, verbose_name="name")),
                ("text", models.TextField(verbose_name="text")),
                (
                    "image",
                    models.ImageField(
                        upload_to=recipes.models.user_directory_path,
                        verbose_name="image",
                    ),
                ),
                (
                    "cooking_time",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="cooking time",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipes",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="author",
                    ),
                ),
                (
                    "ingredients",
                    models.ManyToManyField(
                        related_name="recipes",
                        through="recipes.IngredientRecipe",
                        to="recipes.ingredient",
                    ),
                ),
            ],
            options={
                "verbose_name": "recipe",
                "verbose_name_plural": "recipes",
                "ordering": ("-created", "name"),
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "slug",
                    models.SlugField(max_length=64, unique=True, verbose_name="slug"),
                ),
                (
                    "name",
                    models.CharField(max_length=64, unique=True, verbose_name="name"),
                ),
                (
                    "color",
                    models.CharField(
                        help_text="Color in RGB #RRGGBB format",
                        max_length=7,
                        unique=True,
                        verbose_name="color",
                    ),
                ),
            ],
            options={
                "verbose_name": "tag",
                "verbose_name_plural": "tags",
                "ordering": ("slug", "-created"),
            },
        ),
        migrations.CreateModel(
            name="TagRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recipes.recipe"
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recipes.tag"
                    ),
                ),
            ],
            options={
                "verbose_name": "recipe's tag",
                "verbose_name_plural": "recipe's tags",
                "ordering": ("-created",),
            },
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                related_name="recipes", through="recipes.TagRecipe", to="recipes.tag"
            ),
        ),
        migrations.AddField(
            model_name="ingredientrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_recipes",
                to="recipes.recipe",
            ),
        ),
        migrations.AddConstraint(
            model_name="ingredient",
            constraint=models.UniqueConstraint(
                fields=("name", "measurement_unit"), name="unique_ingredient"
            ),
        ),
        migrations.AddField(
            model_name="incartrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="recipes.recipe"
            ),
        ),
        migrations.AddField(
            model_name="incartrecipe",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart_recipes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="favoriterecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorited_by",
                to="recipes.recipe",
                verbose_name="favorited_by",
            ),
        ),
        migrations.AddField(
            model_name="favoriterecipe",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite_recipes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="favorite",
            ),
        ),
        migrations.AddConstraint(
            model_name="recipe",
            constraint=models.UniqueConstraint(
                fields=("name", "author"), name="unique_recipe"
            ),
        ),
        migrations.AddConstraint(
            model_name="ingredientrecipe",
            constraint=models.UniqueConstraint(
                fields=("ingredient", "recipe", "amount"),
                name="unique_ingredient_recipe",
            ),
        ),
        migrations.AddConstraint(
            model_name="incartrecipe",
            constraint=models.UniqueConstraint(
                fields=("recipe", "user"), name="unique_recipe_in_cart"
            ),
        ),
        migrations.AddConstraint(
            model_name="favoriterecipe",
            constraint=models.UniqueConstraint(
                fields=("recipe", "user"), name="unique_favorite"
            ),
        ),
    ]
