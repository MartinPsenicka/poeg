from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import PaymentTransaction, Voucher, GopayLog
from ..games.models import ActiveGame
from .utils import apply_discount_voucher

class GoPayLogInline(admin.StackedInline):
    model = GopayLog
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'variable_symbol', 'price', 'note')
    list_filter = ('payment_type', 'game', 'ts_created', 'ts_paid', 'instruction_email_sent',)
    search_fields = ('user__email', 'game', 'variable_symbol')

    inlines = [GoPayLogInline]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields if not f.name in ("note", "ts_paid")]

    def save_model(self, request, obj, form, change):
        if obj.ts_paid is not None:
            ActiveGame.objects.create(
                game=obj.game,
                user=obj.user,
                activation_type=ActiveGame.ACTIVATION_TYPE_CHOICES.bankwire
            )
            apply_discount_voucher(obj)
            subject = "Úspěsně zaplacená hra"
            message = render_to_string("email/bankwire_paid.txt")
            try:
                send_mail(subject, message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[obj.user_email])
            except Exception:
                pass
        super(PaymentTransactionAdmin, self).save_model(request, obj, form, change)


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('voucher', 'used_count', 'discount', 'target_price')
    list_filter = ('voucher', 'used_count', 'discount', 'target_price')
    search_fields = ('voucher',)
    # readonly_fields = ('user','game')


@admin.register(GopayLog)
class GoPayLogAdmin(admin.ModelAdmin):
    pass
