import json

from django.db import transaction
from django.db.models import Q
from django.forms import model_to_dict
from django.urls import reverse
from django.views.generic import RedirectView

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile, TrainerProfile, TraineeProfile, BodyInfo
from .services import (
    authenticate_provider, user_login_from_authview,
    GoogleAuthService, UserService
)
from .serializer import (
    AuthSerializer, LoginSerializer, UserProfileSerializer, BodyInfoSerializer, TrainerProfileSerializer
)
from tags.models import HashTag
from tags.serializer import HashTagSerializer


# access_token 및 id_token 권한인증(GET)
class AuthView(RedirectView, generics.RetrieveAPIView):
    serializer_class = AuthSerializer

    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        response = {'validation': {}, 'user': {}}

        auth_serializer = self.serializer_class(data=data)
        auth_serializer.is_valid(raise_exception=True)
        auth_serialized_data = auth_serializer.data

        provider_validation = authenticate_provider(provider=auth_serialized_data['provider'])
        if provider_validation is False:
            return Response({'invalidProvider': False}, status=status.HTTP_400_BAD_REQUEST)
        response['validation']['provider'] = 'success'

        auth_service = GoogleAuthService()
        user_validation = auth_service.google_validate_email(data=auth_serialized_data)
        if user_validation is False:
            return Response({'invalidUser': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response['validation']['email'] = 'success'

        response['user']['info'] = auth_serialized_data
        try:
            user = UserProfile.objects.get(
                Q(oauth_type=data['provider']),
                Q(oauth_token=data['oauth'])
            )
            return user_login_from_authview(user=user)
        except UserProfile.DoesNotExist:
            response['user']['status'] = 'new'
            return Response(response, status=status.HTTP_200_OK)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (IsAuthenticated,)

    # Login Request
    # header    : Authorization: 'Bearer [access_token]'
    # body      : {'email' : [email]}

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 로그인 및 회원가입(POST), 회원정보수정(PUT/PATCH), 회원탈퇴(DELETE)
class UserView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer

    def user_profile_using_serializer(self, data):
        user_service = UserService(data=data)
        serializer = self.serializer_class(
            data=model_to_dict(user_service.set_user_profile_info())
        )
        serializer.is_valid(raise_exception=True)
        return serializer

    def hashtag_using_serializer(self, data):
        serializer = HashTagSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        tags_list = json.loads(json.dumps(serializer.data[:]))
        return tags_list

    def trainee_profile_using_serializer(self, data, tags_list):
        serializer = BodyInfoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        body_info_obj = BodyInfoSerializer().create(serializer.data)
        body_info_obj.save()

        trainee = TraineeProfile.objects.create(body_info=body_info_obj)
        for t in tags_list:
            h = HashTag.objects.create(tag_type=t['tag_type'], tag_content=t['tag_content'])
            trainee.purpose.add(h)
        trainee.save()
        return trainee, trainee.pk

    def trainer_profile_using_serializer(self, data, tags_list):
        serializer = TrainerProfileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        trainer = TrainerProfileSerializer().create(serializer.data)
        for t in tags_list:
            h = HashTag.objects.create(tag_type=t['tag_type'], tag_content=t['tag_content'])
            trainer.specialty.add(h)
        trainer.save()
        return trainer, trainer.pk

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        # 1. 기본정보 profile정보를 serialize화(구글 제공 정보, 추가 입력 정보 저장)
        user_profile_serializer = self.user_profile_using_serializer(data=data)

        with transaction.atomic():
            # 2. UserProfile 객체 생성
            # print(user_profile_serializer.validated_data)
            self.perform_create(user_profile_serializer)
            user_obj = UserProfile.objects.get(email=user_profile_serializer.validated_data['email'])

            tags_list = self.hashtag_using_serializer(data=data['user_info']['tags'])

            # 3. user_type(trainee, trainer)에 따라 TraineeProfile/TrainerProfile serialize화, 객체 생성
            if data['user_type'] == 'trainee':
                trainee, pk = self.trainee_profile_using_serializer(
                    data=data['user_info']['body_info'],
                    tags_list=tags_list
                )
                user_obj.trainee=trainee
                # print(trainee)
                # print(trainee.purpose.all())
            else:
                trainer, pk = self.trainer_profile_using_serializer(
                    data=data['user_info'],
                    tags_list=tags_list
                )
                user_obj.trainer=trainer
                # print(trainer)
                # print(trainer.specialty.all())
            user_obj.save()

            # 4. 로그인을 수행하고, token을 발급
            login_serializer = LoginSerializer(data={'email': data['oauth_info']['email']})
            login_serializer.is_valid(raise_exception=True)
            # print(login_serializer.validated_data)

            # 5. user_pk와 token정보를 담아서 응답data를 구성
            response = {
                'user_pk': pk,
                'token': login_serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        print('in')
        # pk로 object열고, 검증한뒤에 update
        pass

    def destroy(self, request, *args, **kwargs):
        pass
