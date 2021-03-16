from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """ Ingredient model """

    name = models.CharField(max_length=255, verbose_name="Ingredient name")
    measure = models.CharField(max_length=30, verbose_name="Measure")

    def __str__(self):
        return f'Ingredient: {self.name} ({self.measure})'


class Tag(models.Model):
    """ Breakfast, Lunch, Dinner default tags here """
    name = models.CharField(max_length=255, verbose_name="Tag's name")
    color = models.CharField(max_length=100, blank=True,
                             verbose_name="Tag's color")
    nice_name = models.CharField(max_length=255, blank=True,
                                 verbose_name="Nice english name for tag")

    def __str__(self):
        return f'Tag: {self.name}'


class Recipe(models.Model):
    """ Recipe model """

    name = models.CharField(max_length=255, verbose_name="Recipe's title")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="recipes",
                               verbose_name="Recipe's author")
    tags = models.ManyToManyField(Tag, related_name="recipes",
                                  verbose_name="Recipe's tags")
    ingredients = models.ManyToManyField(
        Ingredient, through="Amount", related_name="recipes",
        verbose_name="Recipe's ingredients"
    )
    description = models.TextField(max_length=1000, verbose_name="Description")
    cook_time = models.PositiveSmallIntegerField(verbose_name="Cooking time")
    image = models.ImageField(upload_to="recipes/", blank=True,
                              verbose_name="Recipe's Image")
    slug = AutoSlugField(populate_from="name", allow_unicode=True, unique=True,
                         editable=True, verbose_name="Slug")
    favorite = models.ManyToManyField(User, blank=True,
                                      related_name="favorite_recipes",
                                      verbose_name="Who added to favorites")
    listed = models.ManyToManyField(User, blank=True,
                                    related_name="listed_recipes",
                                    verbose_name="Who added to cart")
    pub_date = models.DateTimeField(
        verbose_name="Publication date",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

    def __str__(self):
        return f'Recipe: {self.name} by {self.author}'


class Amount(models.Model):
    """ Support model for Ingredient&Recipe ManyToMany relation """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="amounts")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name="amounts")
    amount = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f'Amount: {self.ingredient} by {self.amount}'
