from django.contrib.auth import views as auth_views
from django.urls import path

# from . import views

urlpatterns = [
    # Poprzednio używany widoki logowania.
    # path("login/", views.user_login, name="login"),
    # Obecnie używany widok logowania.
    path("login/", auth_views.LoginView.as_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view, name="logout"),
]
