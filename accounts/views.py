from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm, UserRegistrationForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Uwierzytelnienie zakończyło się sukcesem.")
                else:
                    return HttpResponse("Konto jest zablokowane.")
            else:
                return HttpResponse("Nieprawidłowe dane uwierzytelniające.")
    else:
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html", {"section": "dashboard"})


def logout_view(request):
    logout(request)
    return render(request, "registration/logged_out.html", {})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Utworzenie nowego obiektu użytkownika, bez zapisania w bazie danych.
            new_user = user_form.save(commit=False)
            # Ustawienie wybranego hasła.
            new_user.set_password(user_form.cleaned_data["password"])
            # Zapisanie obiektu user.
            new_user.save()
            return render(
                request, "accounts/register_done.html", {"new_user": new_user}
            )
        else:
            user_form = UserRegistrationForm()
            return render(request, "accounts/register.html", {"user_form": user_form})
