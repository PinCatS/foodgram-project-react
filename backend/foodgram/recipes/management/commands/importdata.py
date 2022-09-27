from recipes.management.base import ImportDataBaseCommand
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe
from users.models import User


class Command(ImportDataBaseCommand):
    models = (
        User,
        Ingredient,
        Tag,
        Recipe,
        TagRecipe,
        IngredientRecipe,
    )
