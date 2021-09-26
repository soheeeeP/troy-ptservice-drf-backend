from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.programs.serializer import ProgramDetailSerializer, EvaluationSerializer
from apps.users.models import TraineeProfile, CoachProfile

from utils.responses import ProgramErrorCollection as error_collection
from utils.swagger import *


# 함께하는 트레이너 정보 보여주기 (GET)
class ProgramCoachView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    queryset = TraineeProfile.objects\
        .prefetch_related('program_set__coach__userprofile').all()

    success_response = openapi.Response(
        'PROGRAM_200_WITH_COACH_SUCCESS_RESPONSE',
    )

    @swagger_auto_schema(
        operation_description='트레이니가 등록한 프로그램의 담당 코치 정보를 보여주는 component',
        manual_parameters=[trainee_profile.id_param()],
        responses={
            200: success_response,
            404:
                error_collection.PROGRAM_404_TRAINEE_PROFILE_DOES_NOT_EXISTS.as_md() +
                error_collection.PROGRAM_404_PROGRAM_SET_ATTRIBUTE_ERROR.as_md() +
                error_collection.PROGRAM_404_COACH_ATTRIBUTE_ERROR.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        trainee = self.get_object()
        program = ProgramDetailSerializer.get_program(obj=trainee)

        if program:
            coach_profile, user_profile = ProgramDetailSerializer.get_coach(obj=program)
            response = {
                'user': user_profile,
                'coach': coach_profile
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_200_OK)


# 트레이너의 dashboard에서 활용할 view
class ProgramTraineeView(generics.GenericAPIView):
    pass


class ProgramView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    queryset = TraineeProfile.objects\
        .prefetch_related('program_set', 'program_set__quest_set', 'program_set__goal').all()
    serializer_class = ProgramDetailSerializer

    success_response = openapi.Response(
        'PROGRAM_200_PROGRAM_DASHBOARD_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='트레이너의 운동 현황 대시보드 component',
        manual_parameters=[trainee_profile.id_param()],
        responses={
            200: success_response,
            404:
                error_collection.PROGRAM_404_TRAINEE_PROFILE_DOES_NOT_EXISTS.as_md() +
                error_collection.PROGRAM_404_PROGRAM_SET_ATTRIBUTE_ERROR.as_md() +
                error_collection.PROGRAM_404_GOAL_ATTRIBUTE_ERROR.as_md() +
                error_collection.PROGRAM_404_QUEST_SET_ATTRIBUTE_ERROR.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        trainee = self.get_object()
        program = self.serializer_class.get_program(obj=trainee)
        if program:
            response = {
                'goal': self.serializer_class.get_goal(obj=program),
                'score': self.serializer_class.get_total_score(obj=program),
                'feedback': self.serializer_class.get_feedback(obj=program)
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_200_OK)


class OfflineClassView(generics.GenericAPIView):
    pass


class CoachEvaluationView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    queryset = CoachProfile.objects.all()
    serializer_class = EvaluationSerializer

    success_response = openapi.Response(
        'PROGRAM_200_COACH_EVALUATION_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='트레이너에 대한 코치의 피드백을 모아보는 component',
        manual_parameters=[coach_profile.id_param()],
        responses={
            200: success_response,
            404:
                error_collection.PROGRAM_404_COACH_PROFILE_DOES_NOT_EXISTS.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        coach = self.get_object()
        response = {
            'evaluation': self.serializer_class.get_coach_evaluation(obj=coach),
            'aggregate': self.serializer_class.get_trainee_aggregate(obj=coach),
            'purpose_tags': self.serializer_class.get_purpose_tags(obj=coach),
            'feedback': self.serializer_class.get_feedback_list(obj=coach)
        }
        return Response(response, status=status.HTTP_200_OK)


# 트레이니의 운동 목표 설정 (GET), 수정 (PUT)
class TraineeGoalView(generics.RetrieveUpdateAPIView):
    pass


# 트레이니의 체중정보 입력 (GET)
class TraineeBodyInfoView(generics.RetrieveAPIView):
    pass
