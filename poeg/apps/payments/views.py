import logging

import gopay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.utils.translation import gettext
from django.views.decorators.http import require_POST
from gopay.enums import PaymentInstrument, Currency

from poeg.apps.payments.forms import OrderNewGameForm
from .models import PaymentTransaction, GopayLog, Voucher
from .utils import get_gopay_transaction_status
from ..games.models import Game

log = logging.getLogger('poeg.payments')


# TODO: looks unused
# @login_required
# def confirm_payment(request, game_id):
#     game = get_object_or_404(Game, pk=game_id)
#     form = OrderNewGameForm(request.POST)
#
#     context = dict(
#         game=game
#     )
#
#     if request.method == 'post':
#         if form.is_valid():
#
#             context.update(
#                 price=form.cleaned_data.get("number_of_players", ""),
#                 voucher=form.cleaned_data.get('discount_voucher'),
#             )
#
#     return render(request, "confirm_payment.html", context=context)


@login_required
@require_POST
def bankwire_payment(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    order_form = OrderNewGameForm(request.POST, prefix='order_form')

    if not order_form.is_valid():
        messages.error(request, gettext('Invalid order, please try it again.'))
        return redirect(reverse('activate_game', args=(game.id,)))

    pp = PaymentTransaction.objects.create(
        game=game,
        user=request.user,
        price=order_form.price,
        due_days=7,
        user_email=request.user.email,
        game_name=game.safe_translation_getter('name'),
        variable_symbol=PaymentTransaction.generate_variable_symbol(),
        voucher=order_form.cleaned_data.get('discount_voucher', None),
    )
    context = dict(
        ordered_game=pp,
        price=order_form.cleaned_data['number_of_players']
    )
    subject = "Platební údaje pro Vaši hru"
    message = render_to_string("email/bankwire.txt", context=context, request=request)
    try:
        send_mail(subject, message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[pp.user_email])
        pp.instruction_email_sent = True
        pp.save()
    except Exception:
        pass
    return render(request, "bankwire.html", context=context)


@login_required
@require_POST
def gopay_payment(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    order_form = OrderNewGameForm(request.POST, prefix='order_form')

    if not order_form.is_valid():
        messages.error(request, gettext('Invalid order, please try it again.'))
        return redirect(reverse('activate_game', args=(game.id,)))

    pp = PaymentTransaction.objects.create(
        payment_type=PaymentTransaction.TRANSACTION_TYPES.gopay,
        game=game,
        user=request.user,
        price=order_form.price,
        due_days=1,
        user_email=request.user.email,
        game_name=game.safe_translation_getter('name'),
        variable_symbol=PaymentTransaction.generate_variable_symbol(),
        voucher=order_form.cleaned_data.get('discount_voucher', None),
    )

    api = gopay.payments(settings.GOPAY_CONF)

    gopay_price = int(order_form.price * 100)
    payment_params = dict(
        payer=dict(
            default_payment_instrument=PaymentInstrument.PAYMENT_CARD,
            contact=dict(
                email=request.user.email
            )
        ),
        amount=gopay_price,
        currency=Currency.CZECH_CROWNS,
        order_number=pp.variable_symbol,
        items=[
            dict(
                name=pp.game_name,
                amount=gopay_price,
            )
        ],
        callback=dict(
            return_url=request.build_absolute_uri(reverse('payment-gopay-return', args=(pp.id,))),
            notification_url=request.build_absolute_uri(reverse('payment-gopay-notify', args=(pp.id,)))
        )
    )

    resp = api.create_payment(payment_params)

    GopayLog.objects.create(
        transaction=pp,
        data=resp.json,
    )

    if resp.has_succeed():
        gw_url = resp.json['gw_url']
        log.info('GoPay transaction created successfuly', extra=resp.json)
        return redirect(gw_url)
    else:
        log.error('Bad response when creating GoPay transaction', extra=resp.json)

    context = dict(
        game=game,
        price=pp.price,
    )
    log.info('gopay_payment_created', extra=dict(resp=resp.json, req=payment_params))
    return render(request, "confirm_payment.html", context=context)


@login_required
def gopay_return(request, transaction_id):
    try:
        ctx = get_gopay_transaction_status(transaction_id=transaction_id, query_params=request.GET)
    except Exception as e:
        log.error(e, exc_info=True, extra=dict(transaction_id=transaction_id))
        messages.error(request, gettext('Problem with GoPay payment, please try it again.'))
        return redirect(reverse('homepage'))

    return render(request, "gopay_return.html", context=ctx)


def gopay_notify(request, transaction_id):
    try:
        ctx = get_gopay_transaction_status(transaction_id=transaction_id, query_params=request.GET)
        log.info('Gopay notify received for transaction %s' % transaction_id, extra=ctx)
        status_code = 200
    except Exception as e:
        status_code = 400
        log.error(e, exc_info=True, extra=dict(transaction_id=transaction_id))

    return HttpResponse(status=status_code)


@login_required
@require_POST
def update_voucher_by_dealer(request):
    Voucher.objects.filter(voucher=request.POST.get('voucher'), dealer=request.user).update(
        note=request.POST.get('note'),
        given=bool(request.POST.get('given'))

    )
    return redirect(reverse('my_profile'))
