import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.models import *
from api.users.services import UserService
from api.users.serializer import (
    UserProfileSerializer, TraineeSubProfileSerializer, CoachSubProfileSerializer,
    JWTSerializer, UserProfileCreateUpdateSerializer, LoginSignUpResponseSerializer
)
from apps.programs.models import Program
from api.programs.serializer import ProgramDetailSerializer

from utils.responses import UserErrorCollection as error_collection
from utils.swagger import DuplicateCheckParamCollection as duplicate_check_param_collection
from utils.authentication import TroyJWTAUthentication


class DuplicateCheckView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()

    success_response = openapi.Response(
        'USER_200_DUPLICATE_CHECK_RESPONSE',
        examples={
            'application/json': {
                'nickname': 'bool'
            }
        }
    )

    @swagger_auto_schema(
        manual_parameters=[
            duplicate_check_param_collection.nickname,
        ],
        operation_description='사용자 닉네임 중복여부를 확인합니다.',
        responses={
            200: success_response,
            400:
                error_collection.USER_400_DUPLICATE_CHECK_PARAMETER_ERROR.as_md() +
                error_collection.USER_400_DUPLICATE_CHECK_VALIDATION_ERROR.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        nickname = request.GET.get('nickname', None)
        if nickname:
            try:
                self.queryset.get(nickname__iexact=nickname)
                raise ValidationError('이미 사용중인 닉네임입니다.')
            except UserProfile.DoesNotExist:
                response = {'nickname': True}
                return Response(response, status=status.HTTP_200_OK)

        raise ValidationError('중복 확인을 수행할 data 종류를 parameter로 전달해주세요')


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
            program = trainee.program_set.latest('started_date')
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

