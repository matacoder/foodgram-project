import csv
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from recipe.forms import RecipeForm
from recipe.models import Ingredient, Recipe, Tag
from recipe.services import (combine_ingredients, generate_pdf, get_tags_from,
                             save_form_m2m)
from users.models import User

PER_PAGE = 3


def index(request):
    tags = get_tags_from(request)
    if tags:
        recipes = Recipe.objects.select_related(
            "author",
        ).order_by("-pub_date").filter(tags__name__in=tags).distinct()
    else:
        recipes = Recipe.objects.select_related(
            "author",
        ).order_by("-pub_date").all()

    paginator = Paginator(recipes, PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "index.html",
        {
            "page": page,
            "paginator": paginator,
            "tags": tags,
            "tags_objects": Tag.objects.all(),
        }
    )


def author_recipe(request, username):
    tags = get_tags_from(request)
    author = get_object_or_404(User, username=username)

    if tags:
        recipes = Recipe.objects.select_related(
            "author",
        ).order_by("-pub_date").filter(tags__name__in=tags,
                                       author=author).distinct()
    else:
        recipes = Recipe.objects.select_related(
            "author",
        ).order_by("-pub_date").filter(author=author)

    paginator = Paginator(recipes, PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "recipe/author_recipe.html",
        {
            "page": page,
            "paginator": paginator,
            "author": author,
            "tags_objects": Tag.objects.all(),
            "tags": tags,
        }
    )


@login_required()
def favorite(request):
    tags = get_tags_from(request)
    if tags:
        recipes = request.user.favorite_recipes.select_related(
            "author",
        ).order_by("-pub_date").filter(tags__name__in=tags).distinct()
    else:
        recipes = request.user.favorite_recipes.select_related(
            "author",
        ).order_by("-pub_date").all()

    paginator = Paginator(recipes, PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "recipe/favorite.html",
        {
            "page": page,
            "paginator": paginator,
            "tags_objects": Tag.objects.all(),
            "tags": tags,
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
        {
            "form": form,
        },
    )


@login_required()
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    url = reverse(
        "index",
    )
    if recipe.author == request.user:
        recipe.delete()
    return redirect(url)


@login_required()
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    url = reverse(
        "single",
        kwargs={"slug": slug}
    )
    if recipe.author != request.user:
        return redirect(url)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
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
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

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


@login_required()
def my_follow(request):
    authors = request.user.following.all()

    paginator = Paginator(authors, PER_PAGE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "recipe/my_follow.html",
        {
            "authors": page,
            "paginator": paginator
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
            found_ingredients = Ingredient.objects.filter(
                name__startswith=query)
            for found_ingredient in found_ingredients:
                ingredient_api = {
                    "title": found_ingredient.name,
                    "dimension": found_ingredient.measure,
                }
                data.append(ingredient_api)
    return JsonResponse(data, safe=False)  # Serialize non-dict object


@login_required()
def download_as_pdf(request):
    combined_ingredients = combine_ingredients(request)
    buffer = generate_pdf(combined_ingredients)

    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


@login_required()
def download_as_csv(request):
    combined_ingredients = combine_ingredients(request)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ingredients.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    for key, value in combined_ingredients.items():
        writer.writerow([key, value])

    return response


def server_error(request):
    return render(request, "misc/500.html", status=500)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )
