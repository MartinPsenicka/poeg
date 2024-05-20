from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from ..users.models import User
from ..games.models import Game, Quest, Hint, ActiveGame, ActiveGameLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = []

class HintSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField()
    class Meta:
        model = Hint
        exclude = []


class QuestSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField()
    hints = HintSerializer(many=True, source='hint_set')
    class Meta:
        model = Quest
        exclude = []




class GameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    quests = QuestSerializer(many=True, source='quest_set')


    @staticmethod
    def get_name(obj):
        return obj.name

    class Meta:
        model = Game
        exclude = []


class ActiveGameSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    class Meta:
        model = ActiveGame
        exclude = []

# class ActiveGameLogSerializer(serializers.ModelSerializer):
#     active_game = ActiveGameSerializer()
#     class Meta:
#         model = ActiveGameLog
#         exclude = []