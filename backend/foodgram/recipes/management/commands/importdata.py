from recipes.management.base import ImportDataBaseCommand
from recipes.models import Ingredient, Tag


class Command(ImportDataBaseCommand):
    models = (
        Ingredient,
        Tag,
    )
