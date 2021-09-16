import typing

from django.db.models import Avg, Func
from rest_framework import serializers

from django.db.models.query import QuerySet

from .models import Goal, Service
from users.models import UserProfile, TraineeProfile
from users import serializer as users
from quests.models import Quest


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


class ServiceDetailSerializer(serializers.ModelSerializer):
    coach = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    goal = serializers.SerializerMethodField()
    quest = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['coach']

    @staticmethod
    def get_service(obj: TraineeProfile) -> typing.Optional[Service]:
        if Service.objects.filter(trainee_id=obj.id).exists() is not True:
            return None
        return Service.objects.filter(trainee_id=obj.id).latest('start_date')

    @staticmethod
    def get_coach(obj: TraineeProfile) -> typing.Optional['users.UserProfileDefaultSerializer']:
        if Service.objects.filter(trainee_id=obj.id).exists() is not True:
            return None

        service = Service.objects.filter(trainee_id=obj.id).latest('start_date')
        coach_user = UserProfile.objects.get(coach__service=service)
        return users.UserProfileDefaultSerializer(instance=coach_user).data

    @staticmethod
    def get_goal(obj: TraineeProfile) -> typing.Optional[GoalSerializer]:
        try:
            goal = Service.objects.get(trainee_id=obj.id).goal
            return GoalSerializer(instance=goal).data
        except Service.DoesNotExist:
            return None
        except AttributeError:
            return None

    @staticmethod
    def get_quest(obj: Service):
        if Quest.objects.filter(service_id=obj.id).exists():
            return None
        return Quest.objects.filter(service_id=obj.id).all()

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

