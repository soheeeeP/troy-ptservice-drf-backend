import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.users.models import *
from api.users.services import UserService
from api.users.serializer import (
    UserProfileSerializer, TraineeSubProfileSerializer, CoachSubProfileSerializer,
    LoginSerializer, SignUpSerializer, LoginSignUpResponseSerializer
)
from api.programs.serializer import ProgramDetailSerializer

from utils.responses import UserErrorCollection as error_collection
from utils.swagger import *


class LoginView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer

    success_response = openapi.Response(
        'USER_200_LOGIN_SUCCESS_RESPONSE',
        schema=LoginSignUpResponseSerializer(partial=True)
    )

    @swagger_auto_schema(
        operation_description='JWT로 oauth 사용자 로그인',
        responses={
            200: success_response,
            400: error_collection.USER_400_LOGIN_REQUEST_INVALID.as_md()
        }
    )
    def post(self, request, *args, **kwargs):
        user = self.serializer_class.get_user(request=request)
        response = UserService.set_login_signup_response_info(
            user=user,
            user_type=user.user_type
        )
        return Response(response, status=status.HTTP_201_CREATED)


class SignUpView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = SignUpSerializer

    success_response = openapi.Response(
        'OAUTH_200_SIGNUP_SUCCESS_RESPONSE',
        schema=LoginSignUpResponseSerializer(partial=True)
    )

    @swagger_auto_schema(
        operation_description='oauth 사용자 회원가입',
        responses={
            200: success_response,
            400: error_collection.USER_400_SIGNUP_REQUEST_INVALID.as_md()
        }
    )
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_service = UserService(data=data)
        user_dict = user_service.set_user_profile_info()
        user_serializer = self.serializer_class(data=user_dict, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user, pk = user_serializer.save()

        response = UserService.set_login_signup_response_info(
            user=user,
            user_type=user.user_type
        )
        return Response(response, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


class UserProfileView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    queryset = UserProfile.objects.all().select_related('trainee', 'coach')
    serializer_class = UserProfileSerializer

    success_response = openapi.Response(
        'USER_200_PROFILE_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='사용자 메인 프로필',
        manual_parameters=[user_profile.id_param()],
        responses={
            200: success_response,
            404:
                error_collection.USER_404_PROFILE_ATTRIBUTE_ERROR.as_md() +
                error_collection.USER_404_PROFILE_DOES_NOT_EXISTS.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        user_data = self.serializer_class(instance=user).data
        response = {
            'user': user_data
        }
        if user.user_type == UserProfile.USER_CHOICES.coach:
            return Response(response, status=status.HTTP_200_OK)

        try:
            trainee = user.trainee
        except AttributeError:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        tags = trainee.purpose.values_list('tag_content', flat=True)
        response['coach'] = ProgramDetailSerializer.get_coach(obj=trainee)
        response['tag'] = list(tags)

        return Response(response, status=status.HTTP_200_OK)


class TraineeSubProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    queryset = TraineeProfile.objects.all()
    serializer_class = TraineeSubProfileSerializer

    success_response = openapi.Response(
        'USER_200_TRAINEE_PROFILE_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='트레이너 세부 프로필',
        manual_parameters=[trainee_profile.id_param()],
        responses={
            200: success_response,
            404:
                error_collection.USER_404_TRAINEE_PROFILE_DOES_NOT_EXISTS.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        trainee = self.get_object()
        response = {
            'body_info': self.serializer_class.get_body_info(obj=trainee)
        }
        return Response(response, status=status.HTTP_200_OK)


# 트레이너 세부 프로필 (GET)
class CoachSubProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    queryset = CoachProfile.objects.all()
    serializer_class = CoachSubProfileSerializer

    success_response = openapi.Response(
        'USER_200_COACH_PROFILE_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='코치 세부 프로필',
        manual_parameters=[coach_profile.id_param()],
        responses={
            200: success_response,
            404:
                error_collection.USER_404_COACH_PROFILE_DOES_NOT_EXISTS.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        coach = self.get_object()
        response = self.serializer_class(instance=coach).data
        return Response(response, status=status.HTTP_200_OK)
