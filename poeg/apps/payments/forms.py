from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from requests.exceptions import HTTPError

from poeg.libs import slevomat

from .models import SlevomatAction, PaymentTransaction
from ..payments.models import Voucher
from ..games.models import GamePrice

sc = slevomat.Client(token=settings.SLEVOMAT_TOKEN)


class ApplyVoucherForm(forms.Form):
    voucher = forms.CharField(max_length=20, min_length=3)

    def __init__(self, game_id, *args, **kwargs):
        self.game_id = game_id
        super(ApplyVoucherForm, self).__init__(*args, **kwargs)

    def clean_voucher(self):
        code = self.cleaned_data['voucher']

        valid_voucher_exists = Voucher.objects.filter(gratis=True, used_count=0, voucher=code).count()
        if valid_voucher_exists:
            Voucher.objects.filter(gratis=True, used_count=0, voucher=code).update(used_count=1)
            pass
        else:
            try:
                r = sc.check_voucher(code)
            except HTTPError as e:
                e_data = e.response.json()
                raise ValidationError('Neplatný kód voucheru nebo má slevomat potíže (%(message)s)' % e_data['error'])
            except Exception as e:
                raise ValidationError('Vyskytly se problémy při komunikaci se Slevomatem')

            voucher_product_id = r['data']['voucherData']['product']
            try:
                SlevomatAction.objects.get(game_id=self.game_id, product_id=voucher_product_id)
            except SlevomatAction.DoesNotExist:
                raise ValidationError("Neplatný voucher pro tuto hru")

            # all seems OK, try to apply voucher
            try:
                sc.apply_voucher(code)
            except HTTPError:
                raise ValidationError("Voucher se nepodařilo uplatnit, zkuste to prosím znovu")
            except Exception as e:
                raise ValidationError('Vyskytly se problémy při komunikaci se Slevomatem')


class OrderNewGameForm(forms.Form):
    PRICE_CHOICES = (
        (1600, "3-6 hráčů - 1600Kč",),
        (1300, "1-2 hráči - 1300Kč",)
    )
    discount_voucher = forms.CharField(max_length=20, min_length=3, required=False, label="Slevový kupón")
    number_of_players = forms.TypedChoiceField(choices=PRICE_CHOICES, label="Počet hráčů", coerce=int)

    def clean_discount_voucher(self):
        value = self.cleaned_data['discount_voucher']
        if value:
            try:
                return Voucher.objects.get(Q(used_count=0) | Q(multiple_use=True),gratis=False, voucher__iexact=value)
            except:
                raise ValidationError('Neplatný kupón')

    def clean(self):
        price = self.cleaned_data['number_of_players']
        if self.cleaned_data.get('discount_voucher'):
            price -= self.cleaned_data['discount_voucher'].discount.amount
            if self.cleaned_data.get('discount_voucher').target_price:
                price = self.cleaned_data['discount_voucher'].target_price.amount
        self.price = price
