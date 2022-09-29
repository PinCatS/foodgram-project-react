# Generated by Django 4.1.1 on 2022-09-28 16:30

from django.db import migrations, models
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0002_alter_recipe_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                upload_to=recipes.models.user_directory_path, verbose_name="image"
            ),
        ),
    ]