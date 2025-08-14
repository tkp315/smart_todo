from django.urls import path
from . import views

urlpatterns = [
    path("auth/register/", views.register, name="register"),
    path("auth/login/", views.login, name="login"),
    path("auth/logout/", views.logout, name="logout"),
    path("auth/refresh-token/", views.login, name="refresh-token"),
    path("me/", views.user, name="user_details"),
]
