from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import ActiveGame, ActiveGameLog, Quest, Hint


@login_required
def start_game(request, active_game_id):
    active_game = get_object_or_404(ActiveGame, pk=active_game_id,
                                    ts_finished__isnull=True, user_id=request.user.id)

    if request.method == 'POST' and 'start_game' in request.POST:
        quest_to_start = Quest.objects.filter(game_id=active_game.game.id).order_by("order").first()
        ActiveGameLog.objects.get_or_create(
            active_game=active_game,
            quest=quest_to_start,
        )
        return redirect(
            reverse('active_quest', args=(active_game.id,))
        )

    if active_game.activegamelog_set.all().exists():
        return redirect(
            reverse('active_quest', args=(active_game.id,))
        )
    return render(request, 'start_game.html', dict(active_game=active_game))


@login_required
def finish_game(request, active_game_id):
    active_game = get_object_or_404(ActiveGame, pk=active_game_id,
                                    user_id=request.user.id)
    if not active_game.all_quests_done:
        return redirect(
            reverse('active_quest', args=(active_game.id,))
        )
    ctx = dict(
        active_game=active_game
    )

    return render(request, 'finish_game.html', ctx)


@login_required
def between_quests(request, active_game_id):
    last_game_log = ActiveGameLog.objects.select_related('active_game', 'quest').filter(
        active_game_id=active_game_id, active_game__user_id=request.user.id, ts_finish__isnull=False
    ).order_by('-ts_finish').first()
    ctx = dict(
        last_game_log=last_game_log
    )
    return render(request, 'between_quests.html', ctx)


@login_required
@require_POST
def use_hint(request, active_game_id):
    """add hint to used hints and redirect back to active quest page"""
    active_game_log = get_object_or_404(
        ActiveGameLog, active_game_id=active_game_id, ts_finish__isnull=True, active_game__user_id=request.user.id
    )

    if 'hint_to_use' in request.POST:
        hint_to_use = Hint.objects.get(id=request.POST['hint_to_use'])
        active_game_log.used_hints.add(hint_to_use)
        active_game_log.save()

    return redirect(
        reverse('active_quest', args=(active_game_log.active_game_id,))
    )


@login_required
def active_quest(request, active_game_id):
    active_game = get_object_or_404(
        ActiveGame, pk=active_game_id, ts_finished__isnull=True, user_id=request.user.id
    )

    # zaverecna stranka hry
    if active_game.all_quests_done:
        return redirect(
            reverse('finish_game', args=(active_game.id,))
        )
    # prepare context dict
    ctx = {}

    active_log = ActiveGameLog.objects.filter(
        active_game=active_game,
        ts_finish__isnull=True,
    ).select_related('quest').first()

    if not active_log and not request.method == 'POST':
        # probably browser's back button used
        active_log = ActiveGameLog.objects.create(
            active_game=active_game,
            quest=active_game.next_quest
        )

    ctx['active_log'] = active_log

    if request.method == 'POST':
        if 'finish_this_quest' in request.POST:
            # splneni ukolu a presmerovani na between quests
            active_log.ts_finish = timezone.now()
            active_log.save()
            active_game.refresh_from_db()
            if active_game.all_quests_done:
                active_game.ts_finished = timezone.now()
                active_game.save()
                return redirect(
                    reverse('finish_game', args=(active_game.id,))
                )
            return redirect(
                reverse('between_quests', args=(active_game.id,))
            )
        if 'activate_next_quest' in request.POST:
            if active_log:
                return redirect(
                    reverse('active_quest', args=(active_game.id,))
                )

            if active_game.next_quest:
                ActiveGameLog.objects.create(
                    active_game=active_game,
                    quest=active_game.next_quest
                )
                return redirect(
                    reverse('active_quest', args=(active_game.id,))
                )
            else:
                return redirect(
                    reverse('finish_game', args=(active_game.id,))
                )

    return render(request, 'active_quest.html', ctx)
