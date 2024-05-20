from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _

from ..games.models import Game
from .forms import ProfileChangeForm, GenerateDealerVoucherForm


@login_required
def my_profile_view(request):
    if request.user.is_dealer:
        form = GenerateDealerVoucherForm()
        title = _("Dealer's profile")
    else:
        form = ProfileChangeForm(instance=request.user)
        title = _("User's profile")

    if request.method == 'POST':
        if request.user.is_dealer:
            form = GenerateDealerVoucherForm(request.POST)
            if form.is_valid():
                form.generate(request.user)
                return redirect(
                    reverse('my_profile')
                )
        else:
            form = ProfileChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect(
                    reverse('my_profile')
                )

    ctx = dict(
        games=Game.objects.filter(is_active=True),
        form=form,
        title=title
    )
    return render(request, 'account/user_profile.html', ctx)

