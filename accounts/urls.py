from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Poprzednio używany widoki logowania.
    # path("login/", views.user_login, name="login"),
    # Obecnie używany widok logowania.
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    # Adresy URL przeznaczone do obsługi zmiany hasłą.
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
