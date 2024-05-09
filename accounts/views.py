from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from actions.utils import create_action
from common.decorators import ajax_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact


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
            # Utworzenie profilu użytkownika
            profile = Profile.objects.create(user=new_user)
            create_action(new_user, "utworzył konto")
            return render(
                request, "accounts/register_done.html", {"new_user": new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Uaktualnienie profilu zakończyło się sukcesem.")
        else:
            messages.error(request, "Wystąpił błąd podczas uaktualnienia profilu.")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "accounts/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request, "accounts/user/list.html", {"section": "people", "users": users}
    )


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request, "accounts/user/detail.html", {"section": "people", "user": user}
    )


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, "obserwuje", user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "ok"})
