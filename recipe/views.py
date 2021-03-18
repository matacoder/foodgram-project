import csv

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from foodgram.settings import PER_PAGE
from recipe.forms import RecipeForm
from recipe.models import Recipe, Tag
from recipe.services import (
    combine_ingredients, filter_by_tags, generate_pdf, get_session_recipes,
    get_tags_from, import_ingredients_from_csv, save_form_m2m)
from users.models import User


def index(request):
    tags = get_tags_from(request)
    recipes = Recipe.objects.select_related(
        "author",
    ).order_by("-pub_date").all()
    if tags:
        recipes = filter_by_tags(recipes, tags)

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

    recipes = Recipe.objects.select_related(
        "author",
    ).order_by("-pub_date").filter(author=author)

    if tags:
        recipes = filter_by_tags(recipes, tags)

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
    if form.is_valid():
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
    if request.user.is_authenticated:
        recipes = request.user.listed_recipes.select_related(
            "author",
        ).order_by("-pub_date").all()
    else:
        recipes = get_session_recipes(request)

    return render(
        request,
        "recipe/shop_list.html",
        {
            "recipes": recipes,
        }
    )


def single_recipe(request, slug):
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


def download_as_pdf(request):
    combined_ingredients = combine_ingredients(request)
    buffer = generate_pdf(combined_ingredients)

    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")


def download_as_csv(request):
    combined_ingredients = combine_ingredients(request)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="ingredients.csv"'
    response.write(u"\ufeff".encode("utf8"))

    writer = csv.writer(response)
    for key, value in combined_ingredients.items():
        writer.writerow([key, value])

    return response


@login_required()
def import_csv(request):
    import_ingredients_from_csv()
    return redirect("index")
