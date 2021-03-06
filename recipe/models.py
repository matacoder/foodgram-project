from django.db import models

# Create your models here.
"""

Ingredient
- name
- measure

Recipe
- name
- user id
- tags ManyToMany
- description
- cook_time
- photo
- slug

RecipeIngredients
- id recipe
- id ingredient
- numeric measure

Tags
- name

RecipeTags
- id recipe
- id tags


Following
- id user
- id user

Favorite
- id user
- id recipe

List
- id user
- id recipe

"""
