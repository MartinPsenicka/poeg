from django.contrib import admin
from django.utils.safestring import mark_safe
from parler.admin import TranslatableAdmin, TranslatableTabularInline, TranslatableStackedInline

from poeg.apps.games.models import GamePrice
from .models import Game, Quest, Hint, ActiveGame, ActiveGameLog
from ..payments.models import SlevomatAction


class SlevomatActionInlineAdmin(admin.TabularInline):
    model = SlevomatAction
    extra = 1


class QuestInlineAdmin(TranslatableStackedInline):
    model = Quest
    extra = 0
    readonly_fields = 'quest_link',

    def quest_link(self, obj):
        print(obj.id)
        if not obj:
            return '-'
        return mark_safe('<a href="/admin/games/quest/%s/" target="_blank">Open Quest "%s" admin</a>' % (obj.id, obj))


@admin.register(Game)
class GameAdmin(TranslatableAdmin):
    list_display = ('name', 'homepageorder', 'is_active', 'all_languages_column')
    list_filter = ('is_active',)
    search_fields = ('name', 'homepageblock')
    inlines = [SlevomatActionInlineAdmin, QuestInlineAdmin]


@admin.register(GamePrice)
class GamePriceAdmin(admin.ModelAdmin):
    list_display = ('game', 'price', 'number_of_players')
    list_filter = ('game',)
    search_fields = ('game',)


class HintInlineAdmin(TranslatableTabularInline):
    model = Hint
    extra = 1


@admin.register(Quest)
class QuestAdmin(TranslatableAdmin):
    list_display = ('game', 'order', 'get_short_description', 'all_languages_column')
    list_filter = ('game',)
    search_fields = ('game__name', 'description')
    inlines = [HintInlineAdmin]

    def get_short_description(self, obj):
        return obj.description[:150]

    get_short_description.short_description = 'short description'


@admin.register(Hint)
class HintAdmin(TranslatableAdmin):
    list_display = ('quest', 'time_penalty', 'order', 'all_languages_column')
    list_filter = ('quest__game',)
    search_fields = ('text',)


@admin.register(ActiveGame)
class ActiveGameAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'all_quests_done', 'ts_activated', 'ts_finished')


@admin.register(ActiveGameLog)
class ActiveGameLogAdmin(admin.ModelAdmin):
    list_display = ('active_game', 'quest', 'ts_start', 'ts_finish')
