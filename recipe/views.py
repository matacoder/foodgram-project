from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from recipe.forms import RecipeForm
from recipe.models import Recipe, Ingredient
from recipe.services import save_form_m2m


def index(request):
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
        "index.html",
        {
            # "page": page,
            # "paginator": paginator
        }
    )


def author_recipe(request):
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
        "recipe/author_recipe.html",
        {
            # "page": page,
            # "paginator": paginator
        }
    )


def favorite(request):
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
        "recipe/favorite.html",
        {
            # "page": page,
            # "paginator": paginator
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


def edit_recipe(request):
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
        "recipe/recipe_form.html",
        {
            # "page": page,
            # "paginator": paginator
        }
    )


def shoplist(request):
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
        "recipe/shop_list.html",
        {
            # "page": page,
            # "paginator": paginator
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


def purchases(request):
    return JsonResponse({'success': 'true'})


def subscriptions(request):
    return JsonResponse({'success': 'true'})


def favorites(request):
    return JsonResponse({'success': 'true'})


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
