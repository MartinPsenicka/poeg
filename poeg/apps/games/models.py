import datetime
import os

from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from model_utils.choices import Choices
from parler.models import TranslatableModel, TranslatedFields

from ..users.models import User


class Game(TranslatableModel):
    is_active = models.BooleanField(_("active"), default=True,
                                    help_text=_("Designates whether this game is active."))
    homepageorder = models.PositiveSmallIntegerField(_("homepageorder"), null=True, blank=True, unique=True,
                                                     help_text=_("Order on homepage"))

    translations = TranslatedFields(
        name=models.CharField(_("name"), max_length=255, unique=True),
        homepageblock=models.TextField(_("homepageblock"), blank=True),
        modalblock=models.TextField(_("modalblock"), blank=True),
        startpage=models.TextField(_("startpage"), blank=True),
        finishpage=models.TextField(_("finishpage"), blank=True)
    )

    def __str__(self):
        return self.safe_translation_getter('name')

    class Meta:
        ordering = ("homepageorder",)


class GamePrice(models.Model):
    game = models.ForeignKey(Game, verbose_name=_("gameid"), on_delete=models.PROTECT)
    price = MoneyField(_("game price"), max_digits=8, decimal_places=2)
    number_of_players = models.CharField(_("max number of players"), max_length=50)

    class Meta:
        unique_together = (
            ('game', 'number_of_players'),
        )


class Quest(TranslatableModel):
    game = models.ForeignKey(Game, verbose_name=_("gameid"), on_delete=models.PROTECT)
    order = models.PositiveSmallIntegerField(_("order withing game"), blank=True, default=0)

    translations = TranslatedFields(
        description=models.TextField(_("quest description"), blank=True),
        jscode=models.TextField(_("javascript code"), blank=True),
        after_quest=models.TextField(_("text between quests"), blank=True)
    )

    def __str__(self):
        return 'game %s, quest %s (%s)' % (
            self.game, self.order, self.safe_translation_getter('description')[:15]
        )

    class Meta:
        unique_together = (
            ('game', 'order'),
        )


def hint_image_upload_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(
        "hints",
        slugify(instance.quest.game.name),
        str(instance.quest_id),
        "%s%s" % (slugify(filename), extension)

    )


class Hint(TranslatableModel):
    quest = models.ForeignKey(Quest, verbose_name=_("quest"), on_delete=models.PROTECT)
    image = models.ImageField(_("image"), blank=True, null=True, upload_to=hint_image_upload_to)
    time_penalty = models.PositiveIntegerField(_("penalty"), default=0)
    order = models.PositiveSmallIntegerField(_("order withing quest"), blank=True, default=0)

    translations = TranslatedFields(
        text=models.TextField(_("hint"), blank=True),
    )

    @cached_property
    def pretty_penalty(self):
        return datetime.timedelta(seconds=self.time_penalty)

    class Meta:
        unique_together = (
            ('quest', 'order'),
        )
        ordering = ('order',)


class ActiveGame(models.Model):
    ACTIVATION_TYPE_CHOICES = Choices(
        ('gratis_martin', _('gratis Martin')),
        ('gratis_lucka', _('gratis Lucka')),
        ('voucher_own', _('voucher own')),
        ('voucher_slevomat', _('voucher Slevomat')),
        ('bankwire', _('platba převodem')),
        ('gopay', _('platba GoPay')),
    )
    game = models.ForeignKey(Game, verbose_name=_("gameid"), on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    ts_activated = models.DateTimeField(_("activated"), auto_now_add=True)
    ts_finished = models.DateTimeField(_("finished"), null=True, blank=True)
    activation_type = models.CharField(_("activation type"), blank=True, max_length=50, choices=ACTIVATION_TYPE_CHOICES)

    @cached_property
    def total_quest_count(self):
        return self.game.quest_set.all().count()

    @property
    def finished_quests_count(self):
        return self.activegamelog_set.filter(ts_finish__isnull=False).count()

    @property
    def all_quests_done(self):
        return self.total_quest_count == self.finished_quests_count

    @property
    def started(self):
        return self.activegamelog_set.all().exists()

    @property
    def has_opened_quest(self):
        return self.activegamelog_set.filter(ts_finish__isnull=True).exists()

    @property
    def is_active(self):
        return self.ts_finished is None

    @cached_property
    def spent_times(self):
        st = datetime.timedelta()
        pt = datetime.timedelta()
        for l in self.activegamelog_set.all().iterator():
            st += l.spent_time
            pt += l.spent_penalty_time
        return dict(
            time_clean=st,
            time_penalties=pt,
            time_total=st + pt
        )

    @property
    def next_quest(self):
        finished_ids = self.activegamelog_set.exclude(ts_finish__isnull=True).values_list('quest_id', flat=True)
        return Quest.objects.exclude(pk__in=finished_ids).filter(game_id=self.game_id).order_by('order').first()

    def __str__(self):
        return 'user %s plays game %s, started %s, payed %s' % (
            self.user, self.game, self.ts_activated, self.get_activation_type_display()
        )

    class Meta:
        unique_together = (
            ('game', 'user', 'ts_finished'),
        )


class ActiveGameLog(models.Model):
    active_game = models.ForeignKey(ActiveGame, verbose_name=_("active game"), on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, verbose_name=_("active quest"), on_delete=models.CASCADE)
    ts_start = models.DateTimeField(auto_now_add=True)
    ts_finish = models.DateTimeField(null=True, blank=True)
    used_hints = models.ManyToManyField(Hint, blank=True)

    @cached_property
    def spent_time(self):
        ts_end = self.ts_finish.replace(microsecond=0) if self.ts_finish else timezone.now().replace(microsecond=0)
        return ts_end - self.ts_start.replace(microsecond=0)

    @cached_property
    def spent_penalty_time(self):
        pt = datetime.timedelta()
        for hint_penalty in self.used_hints.values_list('time_penalty', flat=True).iterator():
            pt += datetime.timedelta(seconds=hint_penalty)
        return pt

    def __str__(self):
        return 'active quest %s of game %s (gameID %s) of user %s' % (
            self.quest_id, self.active_game.game.name, self.active_game_id, self.active_game.user
        )

    class Meta:
        unique_together = (
            "active_game",
            "quest"
        )
