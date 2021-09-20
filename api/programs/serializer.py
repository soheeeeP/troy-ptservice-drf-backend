import typing

from django.db.models import Avg, Func
from rest_framework import serializers

from django.db.models.query import QuerySet

from apps.programs.models import Goal, Program
from apps.users.models import UserProfile, TraineeProfile
from api.users import serializer as users
from apps.quests.models import Quest


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 0)'


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

    def validate(self, attrs):
        return dict(attrs)

    def create(self, validated_data):
        return super(GoalSerializer, self).create(validated_data)


class ProgramDetailSerializer(serializers.Serializer):
    coach = serializers.SerializerMethodField()
    program = serializers.SerializerMethodField()
    goal = serializers.SerializerMethodField()
    quest = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()

    @staticmethod
    def get_program(obj: TraineeProfile) -> typing.Optional[Program]:
        if Program.objects.filter(trainee_id=obj.id).exists() is not True:
            return None
        return Program.objects.filter(trainee_id=obj.id).latest('start_date')

    @staticmethod
    def get_coach(obj: TraineeProfile) -> typing.Optional['users.UserProfileDefaultSerializer']:
        if Program.objects.filter(trainee_id=obj.id).exists() is not True:
            return None

        program = Program.objects.filter(trainee_id=obj.id).latest('start_date')
        coach_user = UserProfile.objects.get(coach__program=program)
        return users.UserProfileDefaultSerializer(instance=coach_user).data

    @staticmethod
    def get_goal(obj: TraineeProfile) -> typing.Optional[GoalSerializer]:
        try:
            goal = Program.objects.get(trainee_id=obj.id).goal
            return GoalSerializer(instance=goal).data
        except Program.DoesNotExist:
            return None
        except AttributeError:
            return None

    @staticmethod
    def get_quest(obj: Program):
        if Quest.objects.filter(program_id=obj.id).exists():
            return None
        return Quest.objects.filter(program_id=obj.id).all()

    @staticmethod
    def get_total_score(query: QuerySet[Quest]) -> typing.Optional[dict]:
        score = query.values('meal_score', 'workout_score')
        total_score = score.aggregate(
            meal=Round(Avg('meal_score')),
            workout=Round(Avg('workout_score'))
        )
        return total_score

    @staticmethod
    async def update_daily_quest_score(query: QuerySet[Quest]):
        pass

