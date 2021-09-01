import json

from django.forms import model_to_dict

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .services import UserService
from .serializer import (
    LoginSerializer, UserProfileCreateSerializer
)
from tags.serializer import HashTagSerializer
from users.serializer import BodyInfoSerializer
from services.models import *
from services.serializer import GoalSerializer


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


# 트레이니 메인 프로필 조회(GET), 수정(PUT)
class TraineeProfileView(generics.RetrieveUpdateAPIView):
    def __init__(self):
        self.model = UserProfile

    def get_queryset(self, user_pk):
        user = self.model.objects.values('username', 'nickname', 'profile_img', 'gender').get(pk=user_pk)
        trainee = self.model.objects.select_related('trainee').get(pk=user_pk).trainee
        return user, trainee

    def get(self, request, *args, **kwargs):
        # nickname, gender, profile_img, purpose_tag, coach_name
        user_pk = self.kwargs['pk']

        user_data, trainee = self.get_queryset(user_pk=user_pk)
        tags = trainee.purpose.values_list('tag_content', flat=True)
        trainer_data = Service.objects \
            .values_list('trainer__userprofile__nickname', flat=True).filter(trainee=trainee).latest('start_date')

        response = {
            'user_profile': user_data,
            'trainer_name': trainer_data,
            'tag': list(tags)
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        pass


# 트레이니 세부 프로필 (GET)
class TraineeSubProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    lookup_url_kwarg = None

    def get_queryset(self, user_pk):
        return UserProfile.objects.prefetch_related('trainee_id').get(pk=user_pk)

    def get(self, request, *args, **kwargs):
        # { body_type, weight, height }, { due_date, goal }
        user_pk = self.kwargs['pk']

        user = self.get_queryset(user_pk=user_pk)
        trainee = user.trainee

        body_info = trainee.body_info
        online_service = Service.objects.get(trainee=trainee).onlineservice_set
        goal = online_service.latest('start_date').goal

        body_serializer = BodyInfoSerializer(data=model_to_dict(body_info))
        body_serializer.is_valid(raise_exception=True)
        goal_serializer = GoalSerializer(data=model_to_dict(goal))
        goal_serializer.is_valid(raise_exception=True)

        response = {
            'body_info': body_serializer.data,
            'goal': goal_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


# 트레이너 메인 프로필 조회(GET), 수정(PUT)
class TrainerProfileView(generics.RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass


# 트레이너 세부 프로필 (GET)
class TrainerSubProfileView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        pass


# 트레이너에 대한 피드백 모아보기 (GET)
class TrainerEvaluationView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        pass
