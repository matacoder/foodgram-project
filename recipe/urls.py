from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("username/", views.author_recipe, name="author_recipe"),
    path("favorite/", views.favorite, name="favorite"),
]
