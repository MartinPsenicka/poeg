import gopay
from django.conf import settings
from django.utils import timezone

from .models import PaymentTransaction, GopayLog
from ..games.models import ActiveGame


class GopayTransactionError(Exception):
    pass


def get_gopay_transaction_status(transaction_id, query_params):
    try:
        pt = PaymentTransaction.objects.get(pk=transaction_id)
    except PaymentTransaction.DoesNotExist:
        raise GopayTransactionError('PaymentTransaction not found')

    ctx = {
        'pt': pt,
        'success': False
    }

    if 'id' in query_params:
        try:
            gopay_transaction_id = int(query_params['id'])
        except ValueError:
            raise GopayTransactionError('wrong gopay_transaction_id')

        api = gopay.payments(settings.GOPAY_CONF)
        resp = api.get_status(gopay_transaction_id)

        GopayLog.objects.create(
            transaction=pt,
            data=resp.json,
        )

        if resp.has_succeed():
            ctx['order_state'] = resp.json['state']
            ctx['success'] = True
            if ctx['order_state'] == 'PAID':
                order_number = resp.json['order_number']
                if not pt.variable_symbol == order_number:
                    raise GopayTransactionError('variable_symbol != order_number')

                pt.ts_paid = timezone.now()
                pt.save()

                activated_game = ActiveGame.objects.create(
                    game=pt.game,
                    user=pt.user,
                    activation_type=ActiveGame.ACTIVATION_TYPE_CHOICES.gopay
                )

                apply_discount_voucher(pt)

                ctx['activated_game'] = activated_game
        else:
            raise GopayTransactionError('resp.!has_succeed')
            # TODO poslat typ chyby
    return ctx


def apply_discount_voucher(pt):
    if pt.voucher_id:
        pt.voucher.used_count += 1
        pt.voucher.save()
