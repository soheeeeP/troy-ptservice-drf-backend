import json

from django.forms import model_to_dict

from rest_framework import generics, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .services import UserService
from .serializer import (
    LoginSerializer, UserProfileCreateSerializer
)
from tags.serializer import HashTagSerializer
from centers.serializer import CenterSerializer
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
class TraineeProfileView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    lookup_url_kwarg = None
    queryset = UserProfile.objects.select_related('trainee').all()

    def retrieve(self, request, *args, **kwargs):
        # nickname, gender, profile_img, purpose_tag, coach_name
        user_pk = self.kwargs['pk']
        user_data = get_object_or_404(
            self.get_queryset().values('username', 'nickname', 'profile_img', 'gender'),
            pk=user_pk
        )
        trainee = self.get_object().trainee
        tags = trainee.purpose.values_list('tag_content', flat=True)
        response = {
            'user_profile': user_data,
            'tag': list(tags)
        }
        try:
            # exception handling (DoesNotExist)
            # queryset에 .latest()를 적용하여 single instance의 value값을 tuple로 추출
            trainer_data = Service.objects.filter(trainee=trainee)\
                .values_list('trainer__userprofile__nickname', flat=True)\
                .latest('start_date')
            response['trainer'] = trainer_data
            return Response(response, status=status.HTTP_200_OK)
        except Service.DoesNotExist:
            return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # 수정할 정보 구체화 필요
        pass


# 트레이니 세부 프로필 (GET)
class TraineeSubProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    lookup_url_kwarg = None
    queryset = UserProfile.objects.select_related('trainee').all()

    def retrieve(self, request, *args, **kwargs):
        # { body_type, weight, height }, { due_date, goal }
        user_pk = self.kwargs['pk']

        trainee = self.get_object().trainee
        body_info = trainee.body_info
        response = {
            'body_info': BodyInfoSerializer(instance=body_info).data
        }
        try:
            # exception handling (DoesNotExist)
            # queryset에 .latest()를 적용하여 single instance(Service object)를 받아옴
            service = Service.objects.prefetch_related('onlineservice_set').filter(trainee=trainee).latest('start_date')
            if service.onlineservice_set.exists():
                # onlineservice_set에 .latest()를 적용, single instance(OnlineService object)를 get
                # OnlineService의 goal 객체(OneToOne)를 get
                goal = service.onlineservice_set.latest('start_date').goal
                response['goal'] = GoalSerializer(instance=goal).data
                return Response(response, status=status.HTTP_200_OK)
        except Service.DoesNotExist:
            return Response(response, status=status.HTTP_200_OK)


# 트레이너 메인 프로필 조회(GET), 수정(PUT)
class TrainerProfileView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    lookup_url_kwarg = None
    queryset = UserProfile.objects.select_related('trainer').all()

    def retrieve(self, request, *args, **kwargs):
        user_pk = self.kwargs['pk']

        user_data = get_object_or_404(
            self.get_queryset().values('username', 'nickname', 'profile_img', 'gender'),
            pk=user_pk
        )
        trainer = self.get_object().trainer
        tags = trainer.specialty.values_list('tag_content', flat=True)
        trainer_center_data = CenterSerializer(instance=trainer.center).data

        response = {
            'user_data': user_data,
            'trainer_center': trainer_center_data,
            'tags': list(tags)
        }
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # 수정할 정보 구체화 필요
        pass


# 트레이너 세부 프로필 (GET)
class TrainerSubProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    lookup_url_kwarg = None
    queryset = UserProfile.objects.select_related('trainer').all()

    def retrieve(self, request, *args, **kwargs):
        user_pk = self.kwargs['pk']

        trainer = self.get_object().trainer
        # response = {
        #     "center point",
        #     "description":,
        #     "years_career":,
        #     "license":,
        #     "education":
        # }
        return Response(None, status=status.HTTP_200_OK)


# 트레이너에 대한 피드백 모아보기 (GET)
class TrainerEvaluationView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        pass
