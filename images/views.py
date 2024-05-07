from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from common.decorators import ajax_required
from .forms import ImageCreateForm
from .models import Image


@login_required
def image_create(request):
    if request.method == "POST":
        # Formularz został wysłany.
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Dane formularza są prawidłowe.
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # Przypisanie bieżącego użytkownika do elementu.
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Obraz został dodany.")
            # Przekierowanie do widoku szczegółowego dla nowo utworzonego elementu.
            return redirect(new_item.get_absolute_url())
    else:
        # Utworzenie formularza na podstawie danych dostarczonych przez bookmarklet w żądaniu GET.
        form = ImageCreateForm(data=request.GET)

    return render(
        request, "images/image/create.html", {"section": "images", "form": form}
    )


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request, "images/image/detail.html", {"section": "images", "image": image}
    )


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except:
            pass
    return JsonResponse({"status": "ok"})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get("page")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Jeśli zmienna page nie jest liczba całkowitą, wówczas pobierana jest pierwsza strona wyników.
        images = paginator.page(1)
    except EmptyPage:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "images/image/list_ajax.html",
            {"section": "images", "images": images},
        )
    return render(
        request, "images/image/list.html", {"section": "images", "images": images}
    )
