from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Tag(models.Model):
    slug = models.SlugField(_('slug'), max_length=64, unique=True)
    name = models.CharField(_('name'), max_length=64, unique=True)
    color = models.CharField(
        _('color'),
        max_length=7,
        default='#000000',
        help_text=_('Color in RGB #RRGGBB format'),
    )

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Ingredient(models.Model):
    name = models.CharField(_('name'), max_length=256, unique=True)
    measurement_unit = models.CharField(_('measurement unit'), max_length=256)

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')


class Recipe(models.Model):
    name = models.CharField(_('name'), max_length=200)
    text = models.TextField(_('text'))
    is_favorited = models.BooleanField(_('favorited'), default=False)
    is_in_shopping_cart = models.BooleanField(
        _('in shopping cart'), default=False
    )
    image = models.ImageField(_('image'), upload_to='recipes/images/')
    cooking_time = models.PositiveSmallIntegerField(
        _('cooking time'), validators=[MinValueValidator(1)]
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
    )

    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'], name='unique_recipe'
            )
        ]


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        _('amount'),
        validators=[MinValueValidator(1)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe', 'amount'],
                name='unique_ingredient_recipe',
            )
        ]