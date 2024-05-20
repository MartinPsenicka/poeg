import datetime
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User
from ..payments.models import Voucher


class ProfileChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'teamname', 'newsletter')


class GenerateDealerVoucherForm(forms.Form):

    count = forms.IntegerField(max_value=100, min_value=1, label=_("Number of vouchers to generate"))
    discount = forms.DecimalField(max_digits=8, decimal_places=2, max_value=999, label=_("Discount price"))

    def generate(self, user):
        prefix = user.teamname.upper()[:2]
        prefix += datetime.date.today().strftime('%y%m')
        if int(self.cleaned_data['discount']) == 100:
            prefix += 'A'
        elif int(self.cleaned_data['discount']) == 200:
            prefix += 'B'
        elif int(self.cleaned_data['discount']) == 300:
            prefix += 'C'
        elif int(self.cleaned_data['discount']) == 400:
            prefix += 'D'
        elif int(self.cleaned_data['discount']) == 500:
            prefix += 'E'
        elif int(self.cleaned_data['discount']) == 600:
            prefix += 'F'
        elif int(self.cleaned_data['discount']) == 700:
            prefix += 'G'
        elif int(self.cleaned_data['discount']) == 800:
            prefix += 'H'
        elif int(self.cleaned_data['discount']) == 900:
            prefix += 'I'
        else:
            prefix += str(int(self.cleaned_data['discount'])).zfill(3)

        for i in range(self.cleaned_data['count']):
            Voucher.objects.create(
                dealer=user,
                voucher=Voucher.generate_voucher_code(prefix),
                discount=self.cleaned_data['discount'],
            )
