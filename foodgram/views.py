from django.conf.urls import handler404, handler500

handler404 = "recipe.views.page_not_found"  # noqa
handler500 = "recipe.views.server_error"  # noqa
