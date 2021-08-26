import json

from django.db import transaction
from django.forms import model_to_dict

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile, TrainerProfile, TraineeProfile, BodyInfo
from .services import UserService
from .serializer import (
    LoginSerializer, UserProfileSerializer, BodyInfoSerializer, TrainerProfileSerializer
)
from tags.models import HashTag
from tags.serializer import HashTagSerializer
from oauth.services import AuthService
from oauth.serializer import AuthCreateSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (IsAuthenticated,)

    # Login Request
    # header    : Authorization: 'Bearer [access_token]'
    # body      : {'email' : [email]}

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        response = {}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
        # userpk까지 담아서 보낼것!
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 로그인 및 회원가입(POST), 회원정보수정(PUT/PATCH), 회원탈퇴(DELETE)
class SignUpView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer

    def user_profile_using_serializer(self, data):
        auth_service = AuthService(data=data['oauth'])
        auth_serializer = AuthCreateSerializer(data=model_to_dict(auth_service.sef_auth_info()))
        auth_serializer.is_valid(raise_exception=True)
        print(auth_serializer.validated_data)
        with transaction.atomic():
            oauth = auth_serializer.save()
            user_service = UserService(data=data)
            user_serializer = self.serializer_class(
                data=model_to_dict(user_service.set_user_profile_info(oauth=oauth))
            )
            user_serializer.is_valid(raise_exception=True)
            print(user_serializer.validated_data)
        return auth_serializer, user_serializer

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
        auth, user_profile = self.user_profile_using_serializer(data=data)

        with transaction.atomic():
            # 2. UserProfile 객체 생성
            # print(user_profile_serializer.validated_data)
            auth.save()
            user_obj = user_profile.save()
            print(user_obj.email)

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
            login_serializer = LoginSerializer(data={'email': data['base_info']['email']})
            login_serializer.is_valid(raise_exception=True)
            # print(login_serializer.validated_data)

            # 5. user_pk와 token정보를 담아서 응답data를 구성
            response = {
                'user_pk': user_obj.pk,
                'token': login_serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        print('in')
        # pk로 object열고, 검증한뒤에 update
        pass

    def destroy(self, request, *args, **kwargs):
        pass
