from django.urls import path, include

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("profile/", views.profile, name="profile"),
    path("", include("django.contrib.auth.urls")),
]
