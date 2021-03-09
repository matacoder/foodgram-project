from django import template

from recipe.models import Recipe

register = template.Library()


@register.simple_tag
def how_many_listed(user):
    return user.listed_recipes.count()


@register.simple_tag
def how_many_favorites(user):
    return user.favorite_recipes.count()


@register.simple_tag
def how_many_following(user):
    return user.following.count()


@register.simple_tag
def is_favorite(recipe, user):
    return recipe.favorite.filter(id=user.id).exists()


@register.simple_tag
def is_listed(recipe, user):
    return recipe.listed.filter(id=user.id).exists()


@register.simple_tag
def is_following(user_id, user):
    return user.following.filter(id=user_id).exists()
