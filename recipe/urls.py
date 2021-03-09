from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("username/", views.author_recipe, name="author_recipe"),
    path("favorite/", views.favorite, name="favorite"),
    path("new-recipe/", views.new_recipe, name="new_recipe"),
    path("edit-recipe/", views.edit_recipe, name="edit_recipe"),
    path("shoplist/", views.shoplist, name="shoplist"),
    path("recipe/<slug:slug>/", views.single, name="single"),
    path("following/", views.my_follow, name="my_follow"),
    path("purchases/", views.purchases, name="purchases"),  # API
    path("purchases/<int:recipe_id>/", views.purchases_remove, name="purchases_remove"),  # API
    path("subscriptions/", views.subscriptions, name="subscriptions"),  # API
    path("subscriptions/<int:user_id>/", views.subscriptions_remove, name="subscriptions"),  # API
    path("favorites/", views.favorites, name="favorites"),  # API
    path("favorites/<int:recipe_id>/", views.favorites_remove, name="favorites_remove"),  # API
    path("ingredients/", views.ingredients, name="ingredients"),  # API
]
