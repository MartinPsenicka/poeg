from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class OwnUserAdmin(UserAdmin):
    ordering = ['email']
    list_display = ('username', 'email', 'first_name', 'last_name', 'newsletter')
    list_filter = ('newsletter',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'teamname', 'lang', 'newsletter')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_dealer', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )