import datetime
import random
import string

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from model_utils import choices

from ..games.models import Game
from ..users.models import User


class SlevomatAction(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    product_id = models.IntegerField()
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s: %s" % (self.game, self.product_id)

    class Meta:
        unique_together = (
            'game', 'product_id',
        )


class Voucher(models.Model):
    dealer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    voucher = models.CharField(_("voucher code"), max_length=20, unique=True)
    gratis = models.BooleanField(_("gratis game"), default=False)
    used_count = models.SmallIntegerField(_("used count"), default=0, blank=True)
    multiple_use = models.BooleanField(_("multiple usage"), default=False)
    discount = MoneyField(_("discount"), max_digits=8, decimal_places=2, null=True, blank=True)
    target_price = MoneyField(_("target price"), max_digits=8, decimal_places=2, null=True, blank=True)
    given = models.BooleanField(_("given to customer"), default=False)
    note = models.CharField(_("note"), blank=True, max_length=255)

    @classmethod
    def generate_voucher_code(cls, dealer_price_prefix):
        while True:
            code = dealer_price_prefix + ''.join(random.choice(string.digits + string.ascii_uppercase) for x in range(4))
            try:
                cls.objects.get(voucher=code)
                pass
            except cls.DoesNotExist:
                return code

    def __str__(self):
        return self.voucher


class PaymentTransaction(models.Model):
    TRANSACTION_TYPES = choices.Choices(
        (10, 'slevomat', 'Slevomat'),
        (20, 'bank', 'Bank transfer'),
        (30, 'gopay', 'Gopay payment')
    )
    payment_type = models.SmallIntegerField(_("payment type"), blank=True, choices=TRANSACTION_TYPES,
                                            default=TRANSACTION_TYPES.bank)
    game = models.ForeignKey(Game, verbose_name=_("gameid"), on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name=_("user_id"), on_delete=models.PROTECT)
    variable_symbol = models.CharField(_("variable symbol"), max_length=20, unique=True, blank=True)
    price = MoneyField(_("price"), max_digits=8, decimal_places=2)
    ts_created = models.DateTimeField(_("time of creation"), auto_now_add=True, db_index=True)
    instruction_email_sent = models.BooleanField(_("payment instruction email sent"), default=False, db_index=True)
    notifications_send = models.SmallIntegerField(_("number of sent notifications"), default=0)
    ts_paid = models.DateTimeField(_("time of payment"), null=True, db_index=True, blank=True)
    due_days = models.PositiveSmallIntegerField(_("Days of payment due"), null=True, db_index=True)
    note = models.CharField(_("note"), max_length=50, unique=False, blank=True)
    voucher = models.ForeignKey(Voucher, verbose_name=_("voucher"), blank=True, null=True, on_delete=models.PROTECT)

    # blok doplujicich informaci
    user_email = models.EmailField(_("user email"), max_length=150)
    game_name = models.CharField(_("game name"), max_length=50)

    @classmethod
    def generate_variable_symbol(cls):
        while True:
            variable = ''.join(random.choice(string.digits) for x in range(8))
            try:
                cls.objects.get(variable_symbol=variable)
                pass
            except cls.DoesNotExist:
                return variable

    @property
    def due_date(self):
        return (self.ts_created + datetime.timedelta(days=self.due_days)).date()


class GopayLog(models.Model):
    transaction = models.ForeignKey(PaymentTransaction, on_delete=models.PROTECT)
    ts = models.DateTimeField(auto_now_add=True, db_index=True)
    data = JSONField(null=True)

    def __str__(self):
        return "[%s] transaction %s" % (self.ts, self.transaction_id)

    class Meta:
        verbose_name = _('GoPay log entry')
        verbose_name_plural = _('GoPay log entries')
        ordering = ('-ts',)
