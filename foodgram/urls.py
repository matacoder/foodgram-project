from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import include, path

handler404 = "recipe.views.page_not_found"  # noqa
handler500 = "recipe.views.server_error"  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("users.urls")),
    path("", include("recipe.urls")),
]
