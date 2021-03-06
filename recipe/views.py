from django.core.paginator import Paginator
from django.shortcuts import render


# Create your views here.


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


def new_recipe(request):
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
