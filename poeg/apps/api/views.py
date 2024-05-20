from rest_framework import viewsets, permissions, generics, views, response
from ..games.models import Game, ActiveGame, ActiveGameLog
from ..users.models import User

from django.conf import settings

from . import serializers


class UserView(views.APIView):

    def get(self, request, format=None):
        s = serializers.UserSerializer(instance=self.request.user)

        return response.Response(s.data)

    def post(self, request, *args, **kwargs):
        s = serializers.UserSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return response.Response(s.validated_data)
        else:
            return response.Response(s.error_messages)

class GameViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = serializers.GameSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # lang_code = getattr(self.request.user, 'lang', self.request.LANGUAGE_CODE)
        return Game.objects.all().prefetch_related('translations', 'quest_set', 'quest_set__translations', 'quest_set__hint_set', 'quest_set__hint_set__translations')

class ActiveGameViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ActiveGame.objects.all()
    serializer_class = serializers.ActiveGameSerializer

    def get_queryset(self):
        return self.queryset.select_related('game', 'user').filter(user=self.request.user)

# class RetrieveActiveGameLog(generics.RetrieveAPIView):
#     queryset = ActiveGameLog.objects.filter(active_game=self.request.active_game)
#     serializer_class = serializers.ActiveGameLogSerializer
