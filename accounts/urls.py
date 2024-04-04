from django.urls import path

from . import views

urlpatterns = [
    # Widoki logowania.
    path("login/", views.user_login, name="login"),
]
