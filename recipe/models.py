from django.db import models


class Ingredient(models.Model):
    """ Ingredient model """

    name = models.CharField(max_length=255)
    measure = models.CharField(max_length=30)

    def __str__(self):
        return f'Ingredient: {self.name}'


"""

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

Amount
- id recipe
- id ingredient
- numeric measure

Tags
- name

"""
