import datetime
import typing

from django.db.models import Avg, When, Case, Sum, F, Count
from django.db.models.functions import Round
from django.db.models.query import QuerySet

from rest_framework import serializers

from apps.programs.models import Goal, Program, Evaluation
from apps.users.models import UserProfile, TraineeProfile, CoachProfile
from api.users import serializer as users
from apps.quests.models import Quest
from apps.tags.models import HashTag


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
    total_score = serializers.SerializerMethodField()
    feedback = serializers.SerializerMethodField()

    @staticmethod
    def get_program(obj: TraineeProfile) -> typing.Optional[Program]:
        try:
            return obj.program_set.latest('started_date')
        except AttributeError:
            return None

    @staticmethod
    def get_coach(obj: Program):
        try:
            coach_profile = users.CoachSubProfileSerializer(instance=obj.coach).data
            user_profile = users.UserProfileSerializer(instance=obj.coach.userprofile).data
            return coach_profile, user_profile
        except AttributeError:
            return None

    @staticmethod
    def get_goal(obj: Program) -> typing.Optional[GoalSerializer]:
        try:
            return GoalSerializer(instance=obj.goal).data
        except AttributeError:
            return None

    @staticmethod
    def get_total_score(obj: Program) -> typing.Optional[list]:
        try:
            total_score = obj.quest_set\
                .values('meal_score', 'workout_score') \
                .aggregate(
                    meal=Round(Avg('meal_score')),
                    workout=Round(Avg('workout_score'))
                )
            total_score = [{key: str(value)} for key, value in total_score.items()]
            return total_score
        except AttributeError:
            return None

    @staticmethod
    def get_feedback(obj: Program) -> typing.Optional[list]:
        try:
            feedback = obj.quest_set\
                .annotate(date=F('created_at').strftime('%Y-%m-%d'))\
                .values('date', 'rate_feedback', 'quest_feedback')
            return list(feedback)
        except AttributeError:
            return None

    @staticmethod
    async def update_daily_quest_score(query: QuerySet[Quest]):
        pass


class EvaluationSerializer(serializers.Serializer):
    coach_evaluation = serializers.SerializerMethodField()
    trainee_aggregate = serializers.SerializerMethodField()
    purpose_tags = serializers.SerializerMethodField()
    feedback_list = serializers.SerializerMethodField()

    @staticmethod
    def get_coach_evaluation(obj: CoachProfile) -> typing.Optional[dict]:
        evaluation = Evaluation.objects.values('communication', 'care', 'total_rate') \
            .filter(program__coach_id=obj.id).all()
        total_evaluation = evaluation.aggregate(
            communication=Round(Avg('communication')),
            care=Round(Avg('care')),
            total_rate=Round(Avg('total_rate'))
        )
        return total_evaluation

    @staticmethod
    def get_trainee_aggregate(obj: CoachProfile):
        year = datetime.date.today().year
        trainee = UserProfile.objects\
            .annotate(age=year - F('birth_year'))\
            .values('age', 'gender').filter(trainee__program__coach_id=obj.id)

        total_rate = {
            'gender': trainee.aggregate(
                male=Sum(Case(When(gender__exact=UserProfile.GENDER_CHOICES.male, then=1), default=0)),
                female=Sum(Case(When(gender__exact=UserProfile.GENDER_CHOICES.female, then=1), default=0))
            ),
            'age': trainee.aggregate(
                twenties=Sum(Case(When(age__range=[20, 29], then=1), default=0)),
                thirties=Sum(Case(When(age__range=[30, 39], then=1), default=0)),
                fourties=Sum(Case(When(age__range=[40, 49], then=1), default=0)),
                fifties=Sum(Case(When(age__range=[50, 59], then=1), default=0)),
            )
        }
        return total_rate

    @staticmethod
    def get_purpose_tags(obj: CoachProfile) -> typing.Optional[list]:
        purpose = HashTag.objects\
            .values_list('tag_content', flat=True)\
            .annotate(count=Count('tag_content'))\
            .filter(tag_type=HashTag.TAG_CHOICES.purpose, traineeprofile__program__coach_id=obj.id)\
            .order_by('-count')
        return list(purpose)

    @staticmethod
    def get_feedback_list(obj: CoachProfile) -> typing.Optional[list]:
        feedback = Program.objects\
            .annotate(nickname=F('trainee__userprofile__nickname'), text=F('evaluation__text'))\
            .values('nickname', 'text').filter(coach_id=obj.id)
        return list(feedback)
