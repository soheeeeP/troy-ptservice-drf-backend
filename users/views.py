import json

from django.forms import model_to_dict

from rest_framework import generics, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .services import UserService
from .serializer import (
    LoginSerializer, UserProfileCreateSerializer, UserProfileDefaultSerializer,
    TraineeSubProfileSerializer, CoachSubProfileSerializer
)
from centers.serializer import CenterSerializer
from services import serializer as services


class LoginView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer

    # Login Request
    # header    : Authorization: 'Bearer [access_token]'
    # body      : {'email' : [email]}

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        response = {}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 로그인 및 회원가입(POST), 회원정보수정(PUT/PATCH), 회원탈퇴(DELETE)
class SignUpView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserProfileCreateSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_service = UserService(data=data)
        user_dict = user_service.set_user_profile_info()
        user_serializer = UserProfileCreateSerializer(
            # set_user_profile_info()는 UserProfile 객체 생성에 필요한 정보를 담은 dict를 return
            data=user_dict, partial=True
        )
        user_serializer.is_valid(raise_exception=True)
        user_obj, pk = user_serializer.save()

        # 로그인을 수행하고, token을 발급
        login_serializer = LoginSerializer(data={'email': data['base_info']['email']})
        login_serializer.is_valid(raise_exception=True)

        # user_pk와 발급된 token 정보를 담아서 응답 data를 구성
        response = {
            'user_pk': pk,
            'user_type': user_obj.user_type,
            'token': login_serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


class UserProfileView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    queryset = UserProfile.objects.all().select_related('trainee', 'coach')
    serializer_class = UserProfileDefaultSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        print(user)
        user_data = self.serializer_class(instance=user).data
        response = {
            'user': user_data
        }
        print(user.user_type)
        if user.user_type == 'coach':
            return Response(response, status=status.HTTP_200_OK)

        try:
            trainee = user.trainee
        except AttributeError:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        tags = trainee.purpose.values_list('tag_content', flat=True)
        response['coach'] = self.serializer_class.get_coach(obj=trainee)
        response['tag'] = list(tags)

        return Response(response, status=status.HTTP_200_OK)


# 트레이니 세부 프로필 (GET)
class TraineeSubProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    queryset = TraineeProfile.objects.all()
    serializer_class = TraineeSubProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        # { body_type, weight, height }, { due_date, goal }
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

    def retrieve(self, request, *args, **kwargs):
        coach = self.get_object()
        response = self.serializer_class(instance=coach).data
        return Response(response, status=status.HTTP_200_OK)


# 트레이너에 대한 피드백 모아보기 (GET)
class CoachEvaluationView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        pass
