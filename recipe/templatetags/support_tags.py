from django import template

from foodgram.settings import AUTHOR_ITEMS
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
    return user.his_following.count()


@register.simple_tag
def is_favorite(recipe, user):
    return recipe.favorite.filter(id=user.id).exists()


@register.simple_tag
def is_listed(recipe, user):
    return recipe.listed.filter(id=user.id).exists()


@register.simple_tag
def is_following(user_id, user):
    return user.his_following.filter(id=user_id).exists()


@register.simple_tag
def add_get_param(current_url, tag):
    if "?" in current_url:
        return f"{current_url}&tags={tag}"
    return f"{current_url}?tags={tag}"


@register.simple_tag
def delete_get_param(request, tags=None, param=""):
    tags = list(tags)
    tags.remove(param)
    params = "&".join(f"tags={tag}" for tag in tags)
    if "page" in request.GET:
        path = str(request.get_full_path())
        params_with_page = path.split("&")
        if len(params) > 0:
            return f"{params_with_page[0]}&{params}"
        else:
            return f"{params_with_page[0]}"
    return f"?{params}"


@register.simple_tag
def switch_page(request, page_number):
    path = request.get_full_path()
    current_page = request.GET.get("page")
    if "tags" in path and "page" in path:
        return path.replace(f"page={current_page}", f"page={page_number}")
    if "tags" in path and "page" not in path:
        return f"?page={page_number}&{path[2:]}"
    return f"?page={page_number}"


@register.simple_tag
def get_recipes_of(author):
    return Recipe.objects.filter(author=author)[:AUTHOR_ITEMS]


@register.simple_tag
def get_total_numbers_of_recipes(author):
    return Recipe.objects.filter(author=author).count()


@register.simple_tag
def get_session_cart_len(request):
    cart = request.session.get("cart")
    if cart is not None:
        return len(cart)
    return 0


@register.simple_tag
def is_in_session_cart(request, product_id):
    cart = request.session.get("cart")
    if cart is not None:
        if product_id in cart:
            return True
    return False
