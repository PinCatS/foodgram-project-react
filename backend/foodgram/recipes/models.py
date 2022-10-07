from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.mixins import TimeStampedMixin

User = get_user_model()


class Tag(TimeStampedMixin):
    slug = models.SlugField(_('slug'), max_length=64, unique=True)
    name = models.CharField(_('name'), max_length=64, unique=True)
    color = models.CharField(
        _('color'),
        max_length=7,
        unique=True,
        help_text=_('Color in RGB #RRGGBB format'),
    )

    class Meta:
        ordering = ('slug', '-created')
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Ingredient(TimeStampedMixin):
    name = models.CharField(_('name'), max_length=256)
    measurement_unit = models.CharField(_('measurement unit'), max_length=256)

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            )
        ]


def user_directory_path(instance, filename):
    return f'recipes/images/user_{instance.author.id}/{filename}'


class Recipe(TimeStampedMixin):
    name = models.CharField(_('name'), max_length=200)
    text = models.TextField(_('text'))
    image = models.ImageField(_('image'), upload_to=user_directory_path)
    cooking_time = models.PositiveSmallIntegerField(
        _('cooking time'), validators=[MinValueValidator(1)]
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag, through='TagRecipe', related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
    )

    class Meta:
        ordering = ('-created', 'name')
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
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("recipe\'s tag")
        verbose_name_plural = _("recipe\'s tags")


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name=_('ingredient'),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name=_('recipe'),
    )
    amount = models.PositiveSmallIntegerField(
        _('amount'),
        validators=[MinValueValidator(1)],
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("recipe\'s ingredient")
        verbose_name_plural = _("recipe\'s ingredients")
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe', 'amount'],
                name='unique_ingredient_recipe',
            )
        ]


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name=_('favorited_by'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name=_('favorite'),
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('favorite recipe')
        verbose_name_plural = _('favorite recipes')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite',
            )
        ]


class InCartRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_('recipe'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_recipes',
        verbose_name=_('user'),
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('recipe in cart')
        verbose_name_plural = _('recipes in cart')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_in_cart',
            )
        ]
