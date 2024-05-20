from django import forms
from django.utils import timezone
from .models import Subscribtion


class SubscriptionForm(forms.Form):
    email = forms.EmailField()

    def save(self, user=None):
        s, u = Subscribtion.objects.update_or_create(
            email=self.cleaned_data['email'],
            defaults=dict(
                user_id=user,
                ts_subscribed=timezone.now(),
                ts_unsubscribed=None
            )
        )
        return s
