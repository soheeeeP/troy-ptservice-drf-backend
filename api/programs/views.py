from django.db.models import F, Prefetch, Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from api.programs.serializer import ProgramDetailSerializer, EvaluationSerializer
from api.users.serializer import JWTSerializer, UserProfileSerializer, CoachListSerializer
from apps.users.models import TraineeProfile, CoachProfile
from apps.programs.models import Program

from utils.responses import ProgramErrorCollection as error_collection
from utils.swagger import CoachListQueryParamCollection as coach_list_param_collection
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


class CoachListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CoachProfile.objects.select_related('userprofile','center').all()
    serializer_class = CoachListSerializer

    def get_queryset(self):
        q = self.request.query_params.get('q', None)
        nickname_set = self.queryset.filter(userprofile__nickname__contains=q)
        center_set = self.queryset.filter(
            Q(center__name__icontains=q) |
            Q(center__full_address__icontains=q)
        )
        tag_set = self.queryset.filter(specialtytag__tag__tag_content__icontains=q)
        return nickname_set or center_set or tag_set

    success_response = openapi.Response(
        'PROGRAM_200_COACH_LIST_SUCCESS_RESPONSE',
        examples={
            'application/json': {
                'user': UserProfileSerializer().data,
                'coach': {
                    'id': 0,
                    'nickname': 'string',
                    'profile_img': 'http://example.com',
                    "specialty": [],
                    "center": {
                        'id': 0,
                        'name': 'string',
                        'full_address': 'string',
                        'city': 'string',
                        'district': 'string',
                        'town': 'string',
                    },
                    'evaluation': {
                        'communication': 'float',
                        'care': 'float',
                        'total_rate': 'float'
                    }
                }
            }
        }
    )

    @swagger_auto_schema(
        manual_parameters=[
            coach_list_param_collection.option,
            coach_list_param_collection.q,
            coach_list_param_collection.sorting,
            coach_list_param_collection.order_by
        ],
        operation_description='서비스 내의 코치의 리스트를 반환합니다.',
        responses={
            200: success_response,
            404:
                error_collection.PROGRAM_204_COACH_LIST_DOES_NOT_EXISTS.as_md() +
                error_collection.PROGRAM_404_COACH_LIST_SEARCH_VALUE_ERROR.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        user = JWTSerializer().get_user_by_token(
            header=TroyJWTAUthentication().get_header(request=request)
        )

        # 검색 옵션이 지정되어 있는 경우 filter된 queryset을 사용
        option = self.request.query_params.get('option', None)
        if option == 'search':
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.queryset

        # queryset이 존재하지 않는 경우 (서비스 내에 등록된 코치가 없는 경우), 204_NO_CONTENT error 반환
        if queryset is None:
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        # 코치 프로필 정보를 담은 list를 생성
        coach = self.serializer_class.get_coach_list(queryset=queryset)

        # 응답 data 구성
        response = dict()
        response['user'] = UserProfileSerializer(instance=user).data

        # 정렬 옵션이 지정되어 있는 경우, sort()함수를 호출하여 정렬을 내림차순/오름차순 정렬 수행
        sorting = self.request.query_params.get('sorting', None)
        if not sorting:
            response['coach'] = coach
            return Response(response, status=status.HTTP_200_OK)

        order_by = self.request.query_params.get('order_by', None)
        if order_by == 'ascending':
            response['coach'] = sorted(coach, key=lambda score: score['evaluation']['total_rate'])
        elif order_by == 'descending':
            response['coach'] = sorted(coach, key=lambda score: score['evaluation']['total_rate'], reverse=True)
        else:
            message = '\'order_by\' parameter는 \'ascending\'또는 \'descending\'값만을 가질 수 있습니다.'
            raise ValidationError(message)
        return Response(response, status=status.HTTP_200_OK)

