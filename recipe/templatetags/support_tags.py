from django import template

register = template.Library()


@register.simple_tag
def how_many_listed(user):
    return user.listed_recipes.count()


@register.simple_tag
def how_many_favorites(user):
    return user.favorite_recipes.count()