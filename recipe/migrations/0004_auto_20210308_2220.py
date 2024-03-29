# Generated by Django 3.1.7 on 2021-03-08 19:20

import autoslug.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0003_recipe_pub_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipe",
            options={
                "ordering": ("-pub_date",),
                "verbose_name": "рецепт",
                "verbose_name_plural": "рецепты",
            },
        ),
        migrations.AlterField(
            model_name="amount",
            name="amount",
            field=models.DecimalField(
                decimal_places=1,
                max_digits=5,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                allow_unicode=True, editable=False, populate_from="name"
            ),
        ),
    ]
