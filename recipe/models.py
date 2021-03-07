from django.db import models

# Create your models here.
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
