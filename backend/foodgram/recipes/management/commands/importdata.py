from recipes.management.base import ImportDataBaseCommand
from recipes.models import Ingredient, Tag
from users.models import User


class Command(ImportDataBaseCommand):
    models = (
        Ingredient,
        Tag,
        User,
    )
