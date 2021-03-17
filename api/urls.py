from django.urls import path

from . import views

# API for JS front-end Version 1.0
urlpatterns = [
    path("v1/purchases/", views.purchases, name="purchases"),  # API
    path("v1/purchases/<int:recipe_id>/", views.purchases_remove,
         name="purchases_remove"),  # API
    path("v1/subscriptions/", views.subscriptions, name="subscriptions"),
    # API
    path("v1/subscriptions/<int:user_id>/", views.subscriptions_remove,
         name="subscriptions"),  # API
    path("v1/favorites/", views.favorites, name="favorites"),  # API
    path("v1/favorites/<int:recipe_id>/", views.favorites_remove,
         name="favorites_remove"),  # API
    path("v1/ingredients/", views.ingredients, name="ingredients"),  # API
]