from django.db import models

from ..users.models import User


class Subscribtion(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(unique=True)

    ts_subscribed = models.DateTimeField(auto_now_add=True)
    ts_unsubscribed = models.DateTimeField(null=True, db_index=True)

    def __str__(self):
        return "Subscribtion %s" % self.email
