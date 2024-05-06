from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

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
