from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("username/", views.author_recipe, name="author_recipe"),
    path("favorite/", views.favorite, name="favorite"),
    path("new-recipe/", views.new_recipe, name="new_recipe"),
    path("edit-recipe/", views.edit_recipe, name="edit_recipe"),
    path("shoplist/", views.shoplist, name="shoplist"),
    path("recipe/", views.single, name="single"),
    path("following/", views.my_follow, name="my_follow"),
    path("purchases/", views.purchases, name="purchases"),  # API
    path("subscriptions/", views.subscriptions, name="subscriptions"),  # API
    path("favorites/", views.favorites, name="favorites"),  # API
]
