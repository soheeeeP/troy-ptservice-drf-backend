import json

from django.core.cache import caches
from django.db.models import F, Prefetch
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.programs.serializer import ProgramDetailSerializer, EvaluationSerializer
from api.users.serializer import JWTSerializer
from apps.users.models import UserProfile, TraineeProfile, CoachProfile
from apps.programs.models import Program

from utils.responses import ProgramErrorCollection as error_collection
from utils.authentication import TroyJWTAUthentication


# 함께하는 트레이너 정보 보여주기 (GET)
class ProgramCoachView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TraineeProfile.objects.prefetch_related(
        Prefetch(
            'program_set',
            queryset=Program.objects.select_related('coach__userprofile').all()
        )
    )

    success_response = openapi.Response(
        'PROGRAM_200_WITH_COACH_SUCCESS_RESPONSE',
    )

    @swagger_auto_schema(
        operation_description='트레이니가 등록한 프로그램의 담당 코치 정보를 보여주는 component 입니다.',
        responses={
            200: success_response,
            404:
                error_collection.PROGRAM_404_TRAINEE_PROFILE_DOES_NOT_EXISTS.as_md() +
                error_collection.PROGRAM_404_PROGRAM_SET_ATTRIBUTE_ERROR.as_md() +
                error_collection.PROGRAM_404_COACH_ATTRIBUTE_ERROR.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        user = JWTSerializer().get_user_by_token(
            header=TroyJWTAUthentication().get_header(request=request)
        )
        trainee = self.queryset.get(userprofile=user)
        program = ProgramDetailSerializer.get_program(obj=trainee)
        if program:
            coach_profile, user_profile = ProgramDetailSerializer.get_coach(obj=program)
            response = {
                'user': user_profile,
                'coach': coach_profile
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_200_OK)


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
        operation_description='트레이너의 운동 현황 대시보드 component 입니다.',
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
        user = JWTSerializer().get_user_by_token(
            header=TroyJWTAUthentication().get_header(request=request)
        )
        trainee = self.queryset.get(userprofile=user)
        program = self.serializer_class.get_program(obj=trainee)
        if program:
            response = {
                'score': self.serializer_class.get_total_score(obj=program),
                'feedback': self.serializer_class.get_feedback(obj=program)
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_200_OK)


class CoachEvaluationView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CoachProfile.objects.all()
    serializer_class = EvaluationSerializer

    success_response = openapi.Response(
        'PROGRAM_200_COACH_EVALUATION_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='트레이너에 대한 코치의 피드백을 모아보는 component 입니다.',
        responses={
            200: success_response,
            404:
                error_collection.PROGRAM_404_COACH_PROFILE_DOES_NOT_EXISTS.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        user = JWTSerializer().get_user_by_token(
            header=TroyJWTAUthentication().get_header(request=request)
        )
        coach = self.queryset.get(userprofile=user)
        response = {
            'evaluation': self.serializer_class.get_coach_evaluation(obj=coach),
            'aggregate': self.serializer_class.get_trainee_aggregate(obj=coach),
            'purpose_tags': self.serializer_class.get_purpose_tags(obj=coach),
            'feedback': self.serializer_class.get_feedback_list(obj=coach)
        }
        return Response(response, status=status.HTTP_200_OK)


class ProgramRequestView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TraineeProfile.objects.all()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response = {
            'request': {
                'status': True,
                'key': ''
            },
            'message': ''
        }

    success_response = openapi.Response(
        'PROGRAM_200_NEW_COACH_REQUEST_SUCCESS_RESPONSE',
        examples={
            'application/json': {
                'request': {
                    'status': 'bool',
                    'key': 'int'
                },
                'message': ''
            }
        }
    )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'request': openapi.Schema(type=openapi.TYPE_STRING, description='요청 종류'),
                'code': openapi.Schema(type=openapi.TYPE_STRING, description='코치 코드(oauth token)'),
            }
        ),
        operation_description='트레이니의 새로운 코치 등록 요청을 처리합니다.',
        responses={
            200: success_response,
            404:
                error_collection.PROGRAM_400_CACHE_DOES_NOT_EXISTS.as_md() +
                error_collection.PROGRAM_400_NEW_COACH_REQUEST_DUPLICATE_ERROR.as_md() +
                error_collection.PROGRAM_404_COACH_PROFILE_DOES_NOT_EXISTS.as_md() +
                error_collection.PROGRAM_404_TRAINEE_PROFILE_DOES_NOT_EXISTS.as_md()
        }
    )
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = JWTSerializer().get_user_by_token(
            header=TroyJWTAUthentication().get_header(request=request)
        )

        trainee_id = user.id
        trainee_nickname = user.nickname

        coach = UserProfile.objects.values('id', 'nickname').get(oauth__oauth_token=data['code'])
        coach_id = coach['id']
        coach_nickname = coach['nickname']

        troy_cache = caches['apps']

        # cache_row = "apps:program:request:{coach_id}_{trainee_id}"
        # cache_value = "[트레이니_이름]님이 [코치_이름]님께 수업 개설 요청을 보냈어요"
        key = f'program:request:coach{coach_id}_trainee{trainee_id}'
        stored = troy_cache.get(key)
        if stored:
            self.response['request']['status'] = False
            self.response['message'] = '이미 전송된 요청입니다.'
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)

        value = f'{trainee_nickname}님이 {coach_nickname}님께 수업 개설 요청을 보냈어요.'
        troy_cache.set(key, value)
        self.response['request']['key'] = key
        self.response['message'] = f'{coach_nickname}님께 수업 개설 요청이 전송되었어요.'
        return Response(self.response, status=status.HTTP_201_CREATED)


class ProgramResponseView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CoachProfile.objects.all()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response = {
            'response': {
                'status': True,
                'key': ''
            },
            'message': ''
        }

    success_response = openapi.Response(
        'PROGRAM_200_COACH_RESPONSE_SUCCESS_RESPONSE',
        examples={
            'application/json': {
                'request': {
                    'status': 'bool',
                    'key': 'int'
                },
                'message': ''
            }
        }
    )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'response': openapi.Schema(type=openapi.TYPE_STRING, description='응답 종류'),
                'approval': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='요청 승인 여부'),
                'pk': openapi.Schema(type=openapi.TYPE_INTEGER, description='트레이니 프로필 pk'),
            }
        ),
        operation_description='트레이니의 새로운 코치 등록 응답을 처리합니다.',
        responses={
            200: success_response,
            404:
                error_collection.PROGRAM_400_CACHE_DOES_NOT_EXISTS.as_md() +
                error_collection.PROGRAM_400_COACH_REQUEST_DOES_NOT_EXISTS.as_md() +
                error_collection.PROGRAM_404_COACH_PROFILE_DOES_NOT_EXISTS.as_md() +
                error_collection.PROGRAM_404_TRAINEE_PROFILE_DOES_NOT_EXISTS.as_md()
        }
    )
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = JWTSerializer().get_user_by_token(
            header=TroyJWTAUthentication().get_header(request=request)
        )
        coach_id = user.id
        coach_nickname = user.nickname

        trainee = UserProfile.objects.values('id', 'nickname').get(pk=data['pk'])
        trainee_id = trainee['id']
        trainee_nickname = trainee['nickname']

        troy_cache = caches['apps']
        request_key = f'program:request:coach{coach_id}_trainee{trainee_id}'
        stored = troy_cache.get(request_key)
        if not stored:
            self.response['response']['status'] = False
            self.response['message'] = '요청을 찾을 수 없습니다.'
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)

        if data['approval']:
            response_key = f'program:response:approval:coach{coach_id}_trainee{trainee_id}'
            response_value = f'{coach_nickname}님이 {trainee_nickname}님의 수업 개설 요청을 승인했어요.'
        else:
            response_key = f'program:response:refusal:coach{coach_id}_trainee{trainee_id}'
            response_value = f'{coach_nickname}님이 {trainee_nickname}님의 수업 개설 요청을 거절하셨어요.'

        troy_cache.delete(request_key)
        troy_cache.set(response_key, response_value)

        self.response['response']['key'] = response_key
        self.response['message'] = response_value
        return Response(self.response, status=status.HTTP_201_CREATED)
