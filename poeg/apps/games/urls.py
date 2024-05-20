from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^start/$', views.start_game, name='start_game'),
    url(r'^finish/$', views.finish_game, name='finish_game'),
    url(r'^quest/$', views.active_quest, name='active_quest'),
    url(r'^between/$', views.between_quests, name='between_quests'),
    url(r'^use-hint/$', views.use_hint, name='use_hint'),
]
