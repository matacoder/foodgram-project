import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from recipe.models import Ingredient, Recipe
from users.models import User


@require_http_methods("POST")
def purchases(request):
    recipe_id = json.loads(request.body).get("id")
    if recipe_id is None:
        return JsonResponse({"success": False})
    recipe_id = int(recipe_id)

    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user not in recipe.listed.all():
            recipe.listed.add(request.user)
            recipe.save()
        return JsonResponse({"success": True})
    else:
        cart = request.session.get("cart")
        if not cart:
            cart = []
        cart.append(recipe_id)
        request.session["cart"] = cart
        return JsonResponse({"success": True})


@require_http_methods("DELETE")
def purchases_remove(request, recipe_id):
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user in recipe.listed.all():
            recipe.listed.remove(request.user)
            recipe.save()
        return JsonResponse({"success": True})
    else:
        cart = request.session.get("cart")
        cart = list(cart)
        cart.remove(recipe_id)
        request.session["cart"] = cart
        return JsonResponse({"success": True})


@login_required()
@require_http_methods("POST")
def subscriptions(request):
    user_id = json.loads(request.body).get("id")
    if user_id is None:
        return JsonResponse({"success": False})
    user_id = int(user_id)
    if User.objects.filter(pk=user_id).exists():
        following = User.objects.get(pk=user_id)
        if following not in request.user.following.all():
            request.user.following.add(following)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@login_required()
@require_http_methods("DELETE")
def subscriptions_remove(request, user_id):
    if User.objects.filter(pk=user_id).exists():
        unfollowing = User.objects.get(pk=user_id)
        if unfollowing in request.user.following.all():
            request.user.following.remove(unfollowing)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@login_required()
@require_http_methods("POST")
def favorites(request):
    recipe_id = int(json.loads(request.body).get("id"))
    if recipe_id is None:
        return JsonResponse({"success": False})
    recipe_id = int(recipe_id)

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user not in recipe.favorite.all():
        recipe.favorite.add(request.user)
        recipe.save()
    return JsonResponse({"success": True})


@login_required()
@require_http_methods("DELETE")
def favorites_remove(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user in recipe.favorite.all():
        recipe.favorite.remove(request.user)
        recipe.save()
    return JsonResponse({"success": True})


@login_required()
def ingredients(request):
    data = []
    if request.method == "GET":
        query = request.GET.get("query", "")
        if query:
            found_ingredients = Ingredient.objects.filter(
                name__startswith=query)
            for found_ingredient in found_ingredients:
                ingredient_api = {
                    "title": found_ingredient.name,
                    "dimension": found_ingredient.measure,
                }
                data.append(ingredient_api)
    return JsonResponse(data, safe=False)  # Serialize non-dict object
