import json
from functools import reduce

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from recipe.forms import RecipeForm
from recipe.models import Recipe, Ingredient
from recipe.services import save_form_m2m
from users.models import User

ALLOWED_TAGS = ('breakfast', 'lunch', 'dinner',)


def index(request):
    tags = set()
    if "tags" in request.GET:
        tags = set(request.GET.getlist('tags'))
        tags.intersection_update(set(ALLOWED_TAGS))
    # reduce(lambda x, y: x & y, [Q(tags__name__exact=tag) for tag in tags])
    if tags:
        recipes = Recipe.objects.select_related(
            "author",
        ).order_by("-pub_date").filter(tags__name__in=tags).distinct()
    else:
        recipes = Recipe.objects.select_related(
            "author",
        ).order_by("-pub_date").all()

    paginator = Paginator(recipes, 10)
    # показывать по 10 записей на странице.
    page_number = request.GET.get("page")
    # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)
    # получить записи с нужным смещением

    return render(
        request,
        "index.html",
        {
            "page": page,
            "paginator": paginator,
            "tags": tags
        }
    )


def author_recipe(request, username):
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.select_related(
        "author",
    ).order_by("-pub_date").filter(author=author)

    paginator = Paginator(recipes, 10)
    # показывать по 10 записей на странице.
    page_number = request.GET.get("page")
    # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)
    # получить записи с нужным смещением
    return render(
        request,
        "recipe/author_recipe.html",
        {
            "page": page,
            "paginator": paginator,
            "author": author,
        }
    )


@login_required()
def favorite(request):
    recipes = request.user.favorite_recipes.select_related(
        "author",
    ).order_by("-pub_date").all()

    paginator = Paginator(recipes, 10)
    # показывать по 10 записей на странице.
    page_number = request.GET.get("page")
    # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)
    # получить записи с нужным смещением
    return render(
        request,
        "recipe/favorite.html",
        {
            "page": page,
            "paginator": paginator
        }
    )


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_form_m2m(request, form)

        return redirect("single", slug=recipe.slug)

    return render(
        request,
        "recipe/recipe_form.html",
        {"form": form},
    )


@login_required()
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    url = reverse(
        "single",
        kwargs={"slug": slug}
    )
    if recipe.author != request.user:
        return redirect(url)
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    if request.POST and form.is_valid():
        recipe.amounts.all().delete()  # clean ingredients before m2m saving
        save_form_m2m(request, form)
        return redirect(url)
    used_ingredients = recipe.amounts.all()
    edit = True

    return render(
        request,
        "recipe/recipe_form.html",
        {
            "form": form,
            "used_ingredients": used_ingredients,
            "edit": edit,
        }
    )


def shoplist(request):
    recipes = request.user.listed_recipes.select_related(
        "author",
    ).order_by("-pub_date").all()

    paginator = Paginator(recipes, 10)
    # показывать по 10 записей на странице.
    page_number = request.GET.get("page")
    # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)
    # получить записи с нужным смещением
    return render(
        request,
        "recipe/shop_list.html",
        {
            "page": page,
            "paginator": paginator
        }
    )


def single(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(
        request,
        "recipe/single_page.html",
        {
            "recipe": recipe
        }
    )


def my_follow(request):
    # post_list = Post.objects.select_related(
    #     "author", "group"
    # ).order_by("-pub_date").all()
    #
    # paginator = Paginator(post_list, 10)
    # # показывать по 10 записей на странице.
    # page_number = request.GET.get("page")
    # # переменная в URL с номером запрошенной страницы
    # page = paginator.get_page(page_number)
    # # получить записи с нужным смещением
    return render(
        request,
        "recipe/my_follow.html",
        {
            # "page": page,
            # "paginator": paginator
        }
    )


@login_required()
@require_http_methods('POST')
def purchases(request):
    recipe_id = int(json.loads(request.body).get('id'))
    if Recipe.objects.filter(pk=recipe_id).exists():
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user not in recipe.listed.all():
            recipe.listed.add(request.user)
            recipe.save()
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success': 'false'})


@login_required()
@require_http_methods('DELETE')
def purchases_remove(request, recipe_id):
    if Recipe.objects.filter(pk=recipe_id).exists():
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user in recipe.listed.all():
            recipe.listed.remove(request.user)
            recipe.save()
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success': 'false'})


@login_required()
@require_http_methods('POST')
def subscriptions(request):
    user_id = int(json.loads(request.body).get('id'))
    if User.objects.filter(pk=user_id).exists():
        following = User.objects.get(pk=user_id)
        if following not in request.user.following.all():
            request.user.following.add(following)
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success': 'false'})


@login_required()
@require_http_methods('DELETE')
def subscriptions_remove(request, user_id):
    if User.objects.filter(pk=user_id).exists():
        unfollowing = User.objects.get(pk=user_id)
        if unfollowing in request.user.following.all():
            request.user.following.remove(unfollowing)
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success': 'false'})


@login_required()
@require_http_methods('POST')
def favorites(request):
    recipe_id = int(json.loads(request.body).get('id'))
    if Recipe.objects.filter(pk=recipe_id).exists():
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user not in recipe.favorite.all():
            recipe.favorite.add(request.user)
            recipe.save()
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success': 'false'})


@login_required()
@require_http_methods('DELETE')
def favorites_remove(request, recipe_id):
    if Recipe.objects.filter(pk=recipe_id).exists():
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user in recipe.favorite.all():
            recipe.favorite.remove(request.user)
            recipe.save()
        return JsonResponse({'success': 'true'})
    return JsonResponse({'success': 'false'})


@login_required()
def ingredients(request):
    data = []
    if request.method == "GET":
        query = request.GET.get("query", "")
        if query:
            found_ingredients = Ingredient.objects.filter(name__startswith=query)
            for found_ingredient in found_ingredients:
                ingredient_api = {
                    "title": found_ingredient.name,
                    "dimension": found_ingredient.measure,
                }
                data.append(ingredient_api)
    return JsonResponse(data, safe=False)  # Serialize non-dict object
