from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import include, path

from foodgram import views

handler404 = "foodgram.views.page_not_found"  # noqa
handler500 = "foodgram.views.server_error"  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("users.urls")),
    path("", include("recipe.urls")),
    path("404/", views.page_not_found, name="e404"),
    path("500/", views.server_error, name="e500"),
    path("tech/", views.tech, name="tech"),
]
