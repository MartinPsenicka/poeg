from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse

from ..games.models import Game, ActiveGame
from ..newsletter.forms import SubscriptionForm
from ..payments.forms import ApplyVoucherForm
from ..payments.forms import OrderNewGameForm


def homepage_view(request):
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            user_id = request.user.id if request.user.is_authenticated() else None
            s = subscription_form.save(user=user_id)
            messages.success(request, "Děkujeme za přihlášení k odběru newsletteru.")
            return redirect(reverse('homepage'))
    else:
        subscription_form = SubscriptionForm()
    context = dict(
        subscription_form=subscription_form,
        games=Game.objects.filter(is_active=True),
        title="Prague Outdoor Escape Games",
    )
    return render(request, 'homepage.html', context)


@login_required
def activate_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id, is_active=True)
    activate_form = ApplyVoucherForm(game.id, prefix='apply_voucher')
    order_form = OrderNewGameForm(prefix='order_form')

    if request.method == 'POST':
        if 'order_form-number_of_players' in request.POST:
            order_form = OrderNewGameForm(request.POST, prefix='order_form')
            if order_form.is_valid():
                context = dict(
                    order_form=order_form,
                    game=game,
                )
                return render(request, 'confirm_payment.html', context=context)

        else:
            activate_form = ApplyVoucherForm(game.id, request.POST, prefix='apply_voucher')

            if activate_form.is_valid():
                ActiveGame.objects.create(
                    game_id=game_id,
                    user=request.user,
                    activation_type=ActiveGame.ACTIVATION_TYPE_CHOICES.voucher_slevomat
                )
                return redirect(reverse("my_profile"))

    context = dict(
        activate_form=activate_form,
        game=game,
        order_form=order_form
    )
    return render(request, 'activate_game.html', context=context)

# def order_game(request, game_id):
#     game = get_object_or_404(Game, pk=game_id, is_active=True)
#     if request.method == 'POST':
#         order_game = OrderNewGameForm(game.id, request.POST)  #xx
#         if order_game.is_valid():
#             ActiveGame.objects.create(
#                 game_id=game_id,
#                 user=request.user,
#                 activation_type=ActiveGame.ACTIVATION_TYPE_CHOICES.voucher_slevomat
#             )
#             return redirect(reverse("my_profile"))
#     else:
#         order_form = OrderNewGameForm(game.id)  #xx
#     context = dict(
#         # order_game=order_game,
#         game=game,
#         order_form=order_form
#     )
#     # return render(request, 'activate_game.html', context=context)
#     pass
