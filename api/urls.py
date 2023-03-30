from django.urls import include, path

from . import views

# API for JS front-end Version 1.0
urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("purchases/", views.purchases, name="purchases"),  # API
                path(
                    "purchases/<int:recipe_id>/",
                    views.purchases_remove,
                    name="purchases_remove",
                ),  # API
                path("subscriptions/", views.subscriptions, name="subscriptions"),
                # API
                path(
                    "subscriptions/<int:user_id>/",
                    views.subscriptions_remove,
                    name="subscriptions",
                ),  # API
                path("favorites/", views.favorites, name="favorites"),  # API
                path(
                    "favorites/<int:recipe_id>/",
                    views.favorites_remove,
                    name="favorites_remove",
                ),  # API
                path("ingredients/", views.ingredients, name="ingredients"),  # API
            ]
        ),
    )
]
