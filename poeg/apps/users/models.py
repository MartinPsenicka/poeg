from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    objects = UserManager()

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=50, blank=True)
    last_name = models.CharField(_("last name"), max_length=50, blank=True)
    is_active = models.BooleanField(_("active"), default=True,
                                    help_text=_("Designates whether this user should be treated as "
                                                "active. Unselect this instead of deleting accounts."))
    is_staff = models.BooleanField(_("staff status"), default=False,
                                   help_text=_("Designates whether the user can log into this admin site."))
    is_dealer = models.BooleanField(_("voucher dealer"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    teamname = models.CharField(_("teamname"), max_length=50, blank=True, null=True, unique=True,
                                help_text=_("Jméno Vašeho týmu"))

    lang = models.CharField(_("prefered lang"), max_length=5, blank=True, help_text=_("Language ISO."), choices=settings.LANGUAGES)

    newsletter = models.BooleanField(_("informovat o novinkách"), default=True)
    
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        if self.teamname:
            return self.teamname
        return self.first_name

    @property
    def username(self):
        return self.teamname

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
