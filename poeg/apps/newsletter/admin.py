from django.contrib import admin

from .models import Subscribtion


@admin.register(Subscribtion)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'ts_unsubscribed')
    search_fields = ('email',)
