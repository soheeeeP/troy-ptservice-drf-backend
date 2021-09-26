import typing

from rest_framework import serializers

from apps.quests.models import Quest, MealPlanner, Workout


class MealPlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlanner
        fields = '__all__'


class MealPlannerCreateUpdateSerializer(serializers.Serializer):
    pass


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'


class WorkoutCreateUpdateSerializer(serializers.Serializer):
    pass


class QuestDetailSerializer(serializers.ModelSerializer):
    meal_planner = MealPlannerSerializer(read_only=True)
    workout = WorkoutSerializer(read_only=True)
    score = serializers.SerializerMethodField()
    feedback = serializers.SerializerMethodField()

    @staticmethod
    def get_quest_score(obj: Quest) -> typing.Optional[dict]:
        # meal_score, workout_score
        pass

    @staticmethod
    def get_feedback(obj: Quest) -> typing.Optional[dict]:
        # rate_feedback, quest_feedback
        pass


class QuestUpdateSerializer(serializers.ModelSerializer):
    meal_planner = MealPlannerCreateUpdateSerializer(read_only=False)
    workout = WorkoutCreateUpdateSerializer(read_only=False)

    class Meta:
        model = Quest
        fields = ['meal_planner', 'workout', 'rate_feedback', 'quest_feedback', 'meal_score', 'workout_score']

    def update(self, instance, validated_data):
        pass
