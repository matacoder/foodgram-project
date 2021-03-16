from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("u/<str:username>/", views.author_recipe, name="author_recipe"),
    path("favorite/", views.favorite, name="favorite"),
    path("new-recipe/", views.new_recipe, name="new_recipe"),
    path("recipe/<slug:slug>/edit/", views.edit_recipe, name="edit_recipe"),
    path("shoplist/", views.shoplist, name="shoplist"),
    path("shoplist/pdf/", views.download_as_pdf, name="pdf"),
    path("shoplist/csv/", views.download_as_csv, name="csv"),
    path("recipe/<slug:slug>/", views.single_recipe, name="single"),
    path("recipe/<slug:slug>/edit/delete/", views.delete_recipe,
         name="delete"),
    path("following/", views.my_follow, name="my_follow"),
]

# API for JS front-end Version 1.0
urlpatterns += [
    path("api/v1/purchases/", views.purchases, name="purchases"),  # API
    path("api/v1/purchases/<int:recipe_id>/", views.purchases_remove,
         name="purchases_remove"),  # API
    path("api/v1/subscriptions/", views.subscriptions, name="subscriptions"),  # API
    path("api/v1/subscriptions/<int:user_id>/", views.subscriptions_remove,
         name="subscriptions"),  # API
    path("api/v1/favorites/", views.favorites, name="favorites"),  # API
    path("api/v1/favorites/<int:recipe_id>/", views.favorites_remove,
         name="favorites_remove"),  # API
    path("api/v1/ingredients/", views.ingredients, name="ingredients"),  # API
]
