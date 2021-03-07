from django.db import models

from users.models import User


class Ingredient(models.Model):
    """ Ingredient model """

    name = models.CharField(max_length=255)
    measure = models.CharField(max_length=30)

    def __str__(self):
        return f'Ingredient: {self.name} ({self.measure})'


class Tag(models.Model):
    """ Breakfast, Lunch, Dinner default tags here """
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'Tag: {self.name}'


class Recipe(models.Model):
    """ Recipe model """

    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    tags = models.ManyToManyField(Tag, related_name="recipes")
    ingredients = models.ManyToManyField(Ingredient, through="Amount", related_name="recipes")
    description = models.TextField(max_length=1000)
    cook_time = models.IntegerField()
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=200)
    favorite = models.ManyToManyField(User, blank=True, related_name="favorite_recipes")
    listed = models.ManyToManyField(User, blank=True, related_name="listed_recipes")
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f'Recipe: {self.name} by {self.author}'


class Amount(models.Model):
    """ Support model for Ingredient&Recipe ManyToMany relation """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="amounts")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="amounts")
    amount = models.IntegerField()


"""
Database blueprint


AbstractUser
- following Many2Many AbstractUser

Ingredient
- name
- measure

Recipe
- name
- user id
- Tags ManyToMany Tags
- Recipe ManyToMay Ingredient through Amount
- description
- cook_time
- photo
- slug
- favorite ManyToMany AbstractUser
- listed ManyToMany AbstractUser
- pub_date (auto)

Amount
- id recipe
- id ingredient
- numeric measure

Tags
- name

"""
