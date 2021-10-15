import json

from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.models import *
from api.users.services import UserService
from api.users.serializer import (
    UserProfileSerializer, TraineeSubProfileSerializer, CoachSubProfileSerializer, CoachListSerializer,
    JWTSerializer, UserProfileCreateUpdateSerializer, LoginSignUpResponseSerializer
)
from apps.programs.models import Program
from api.programs.serializer import ProgramDetailSerializer

from utils.responses import UserErrorCollection as error_collection
from utils.swagger import CoachListQueryParamCollection as coach_list_param_collection
from utils.authentication import TroyJWTAUthentication


class LoginView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = JWTSerializer
    queryset = UserProfile.objects.all().select_related('trainee', 'coach')

    success_response = openapi.Response(
        'USER_200_LOGIN_SUCCESS_RESPONSE',
        schema=LoginSignUpResponseSerializer(partial=True)
    )

    @swagger_auto_schema(
        operation_description='이메일을 통해 사용자 로그인을 수행한 뒤 JWT를 반환합니다.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='사용자 이메일'),
            }
        ),
        responses={
            200: success_response,
            400: error_collection.USER_400_LOGIN_REQUEST_INVALID.as_md()
        }
    )
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = self.queryset.get(email=data['email'])
        response = UserService.set_login_signup_response_info(
            user=user,
            user_type=user.user_type
        )
        return Response(response, status=status.HTTP_201_CREATED)


class SignUpView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserProfileCreateUpdateSerializer

    success_response = openapi.Response(
        'OAUTH_200_SIGNUP_SUCCESS_RESPONSE',
        schema=LoginSignUpResponseSerializer(partial=True)
    )

    @swagger_auto_schema(
        operation_description='사용자 회원가입을 수행한 뒤, JWT와 등록된 사용자 정보를 반환합니다.',
        responses={
            200: success_response,
            400: error_collection.USER_400_SIGNUP_REQUEST_INVALID.as_md()
        }
    )
    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST['data'])
        user_dict = UserService().set_user_profile_info(data=data, img=request.FILES.get('profile_img'))
        user_serializer = self.serializer_class(data=user_dict, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user, pk = user_serializer.save()

        response = UserService.set_login_signup_response_info(
            user=user,
            user_type=user.user_type
        )
        return Response(response, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        pass


class UserProfileView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all().select_related('trainee', 'coach')
    serializer_class = UserProfileSerializer

    success_response = openapi.Response(
        'USER_200_PROFILE_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='사용자 메인 프로필을 반환하는 component 입니다.',
        responses={
            200: success_response,
            404:
                error_collection.USER_404_PROFILE_ATTRIBUTE_ERROR.as_md() +
                error_collection.USER_404_PROFILE_DOES_NOT_EXISTS.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        user = JWTSerializer().get_user_by_token(
            header=TroyJWTAUthentication().get_header(request=request)
        )
        response = dict()
        response['user'] = self.serializer_class(instance=user).data

        if user.is_staff:
            response['user']['user_type'] = 'superuser'
            return Response(response, status=status.HTTP_200_OK)

        if user.user_type == UserProfile.USER_CHOICES.coach:
            return Response(response, status=status.HTTP_200_OK)

        try:
            trainee = user.trainee
        except AttributeError:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        tags = trainee.purpose.values_list('tag_content', flat=True)
        response['tag'] = list(tags)
        try:
            program = trainee.program_set.latest('created_at')
        except Program.DoesNotExist:
            return Response(response, status=status.HTTP_200_OK)

        response['coach'] = ProgramDetailSerializer.get_coach(obj=program)
        return Response(response, status=status.HTTP_200_OK)


class TraineeSubProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TraineeProfile.objects.all()
    serializer_class = TraineeSubProfileSerializer

    success_response = openapi.Response(
        'USER_200_TRAINEE_PROFILE_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='트레이너 세부 프로필을 반환하는 component 입니다.',
        responses={
            200: success_response,
            404:
                error_collection.USER_404_TRAINEE_PROFILE_DOES_NOT_EXISTS.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        user = JWTSerializer().get_user_by_token(
            header=TroyJWTAUthentication().get_header(request=request)
        )
        if user.is_staff:
            return Response(None, status=status.HTTP_200_OK)

        response = {
            'body_info': self.serializer_class.get_body_info(obj=user.trainee)
        }
        return Response(response, status=status.HTTP_200_OK)


# 트레이너 세부 프로필 (GET)
class CoachSubProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CoachProfile.objects.all()
    serializer_class = CoachSubProfileSerializer

    success_response = openapi.Response(
        'USER_200_COACH_PROFILE_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='코치 세부 프로필을 반환하는 component 입니다.',
        responses={
            200: success_response,
            404:
                error_collection.USER_404_COACH_PROFILE_DOES_NOT_EXISTS.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        user = JWTSerializer().get_user_by_token(
            header=TroyJWTAUthentication().get_header(request=request)
        )
        if user.is_staff:
            return Response(None, status=status.HTTP_200_OK)

        response = self.serializer_class(instance=user.coach).data
        return Response(response, status=status.HTTP_200_OK)


class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileCreateUpdateSerializer

    success_response = openapi.Response(
        'USER_200_PROFILE_PARTIAL_UPDATE_RESPONSE',
        schema=LoginSignUpResponseSerializer(partial=True)
    )

    @swagger_auto_schema(
        operation_description='사용자 프로필 업데이트(코치/트레이니)를 수행합니다.',
        responses={
            200: success_response,
            404:
                error_collection.USER_404_PROFILE_ATTRIBUTE_ERROR.as_md() +
                error_collection.USER_404_COACH_PROFILE_DOES_NOT_EXISTS.as_md() +
                error_collection.USER_404_TRAINEE_PROFILE_DOES_NOT_EXISTS.as_md() +
                error_collection.USER_404_PROFILE_UPDATE_INVALID_DATA_ERROR.as_md()
        }
    )
    def patch(self, request, *args, **kwargs):
        data = json.loads(request.POST['data'])
        user = JWTSerializer().get_user_by_token(
            header=TroyJWTAUthentication().get_header(request=request)
        )
        user_dict = UserService().set_user_profile_info(data=data, img=request.FILES.get('profile_img'))
        user_serializer = self.serializer_class(instance=user, data=user_dict, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        response = UserService.set_login_signup_response_info(
            user=user,
            user_type=user.user_type
        )
        return Response(response, status=status.HTTP_201_CREATED)


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
                error_collection.USER_204_COACH_LIST_DOES_NOT_EXISTS.as_md() +
                error_collection.USER_404_COACH_LIST_SEARCH_VALUE_ERROR.as_md()
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
