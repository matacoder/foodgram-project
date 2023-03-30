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
    path("recipe/<slug:slug>/edit/delete/", views.delete_recipe, name="delete"),
    path("following/", views.my_follow, name="my_follow"),
    path("system/import/csv/", views.import_csv, name="import_csv"),
]
