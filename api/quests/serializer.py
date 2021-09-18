import typing
from decimal import Decimal

from rest_framework import serializers

from apps.quests.models import Quest, Score


class ScoreDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'


class ScoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

    # score객체 생성
    def create(self, validated_data):
        meal_score = validated_data.pop('meal_score')
        workout_score = validated_data.pop('workout_score')


class QuestDetailSerializer(serializers.ModelSerializer):
    quest_score = serializers.SerializerMethodField()
    meal = serializers.SerializerMethodField()
    workout = serializers.SerializerMethodField()

    @staticmethod
    def get_quest_score(obj: Quest) -> typing.Optional[ScoreDefaultSerializer]:
        # quest의 점수 return
        # try:
        #     total_score = obj.score
        # except AttributeError:
        #     return None
        pass

    @staticmethod
    def get_meal(obj: Quest) -> typing.Optional[Decimal]:
        # Quest와 1:1으로 mapping된 MealPlanner객체에 접근, 달성률을 확인하여 Decimal value로 return
        # (clear_field가 True인것 / 3)
        pass

    @staticmethod
    def get_workout(obj: Quest) -> typing.Optional[Decimal]:
        # Quest와 M:M으로 mapping된 Worktout객체에 접근, 달성률을 계산하여 Decimal value로 return
        # (workout_clear_field가 True인 것 / queryset의 전체 객체 수)
        pass


class QuestUpdateSerializer(serializers.ModelSerializer):
    quest_score = ScoreCreateSerializer(read_only=True)

    class Meta:
        model = Quest
        fields = ['rate_feedback', 'quest_feedback', 'quest_score']

    def update(self, instance, validated_data):
        # partial=True 옵션으로 PATCH

        # 1. get_meal()과 get_workout()으로 계산한 점수값으로 Score객체 생성, Quest에 mapping(1:1)
        # 이 때, ScoreCreateSerializer 이용

        # 2. rate_feedback, quest_feedback update
        pass