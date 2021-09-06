# _ProfileSerializer들의 경우, 필요한 정보만 뽑아오도록 수정할 필요가 있음
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, TraineeProfile, TrainerProfile, BodyInfo

from centers.models import Center
from centers.serializer import CenterSerializer
from oauth.serializer import AuthCreateSerializer
from tags.models import HashTag
from tags.serializer import HashTagSerializer

from Troy.settings import base


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'])
        # print(user)
        if user is None:
            raise serializers.ValidationError('invalid login credentials')

        refresh = RefreshToken.for_user(user)
        data = super().validate(attrs)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        # print(data)

        if base.SIMPLE_JWT['UPDATE_LAST_LOGIN'] is True:
            update_last_login(None, user)

        return data


class BodyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyInfo
        fields = '__all__'

    def validate(self, attrs):
        return dict(attrs)

    def create(self, validated_data):
        return super(BodyInfoSerializer, self).create(validated_data)


class TraineeProfileSerializer(serializers.ModelSerializer):
    body_info = BodyInfoSerializer()
    purpose = HashTagSerializer(many=True)

    class Meta:
        model = TraineeProfile
        fields = '__all__'

    def validate(self, attrs):
        return attrs


class TraineeProfileCreateSerializer(serializers.ModelSerializer):
    body_info = BodyInfoSerializer(read_only=False)
    purpose = HashTagSerializer(many=True, read_only=False)

    class Meta:
        model = TraineeProfile
        fields = '__all__'

    def create(self, validated_data):
        body_info = validated_data.pop('body_info')
        body_info_obj = BodyInfo.objects.create(**body_info)

        tags = validated_data.pop('purpose')
        tags_list = [HashTag(tag_type=x['tag_type'], tag_content=x['tag_content']) for x in tags]
        tags_obj = HashTag.objects.bulk_create(tags_list)
        for t in tags_obj:
            t.save()

        trainee = TraineeProfile.objects.create(body_info=body_info_obj)
        trainee.purpose.add(*tags_obj)
        trainee.save()

        return trainee, trainee.pk


class TrainerProfileSerializer(serializers.ModelSerializer):
    center = CenterSerializer()
    specialty = HashTagSerializer(many=True)

    class Meta:
        model = TrainerProfile
        fields = '__all__'

    def validate(self, attrs):
        return attrs


class TrainerProfileCreateSerializer(serializers.ModelSerializer):
    center = CenterSerializer(read_only=False)
    specialty = HashTagSerializer(many=True, read_only=False)

    class Meta:
        model = TrainerProfile
        fields = '__all__'

    def create(self, validated_data):
        center = validated_data.pop('center')
        center_obj = Center.objects.create(**center)

        tags = validated_data.pop('specialty')
        tags_list = [HashTag(tag_type=x['tag_type'], tag_content=x['tag_content']) for x in tags]
        tags_obj = HashTag.objects.bulk_create(tags_list)
        for t in tags_obj:
            t.save()

        trainer = TrainerProfile.objects.create(center=center_obj)
        trainer.specialty.add(*tags_obj)
        trainer.save()

        return trainer, trainer.pk


class UserProfileDefaultSerializer(serializers.ModelSerializer):
    trainee = TraineeProfileSerializer(read_only=True)
    trainer = TrainerProfileSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'nickname', 'gender', 'birth_year', 'profile_img', 'trainee', 'trainer']

    def validate(self, attrs):
        super(UserProfileDefaultSerializer, self).validate(attrs)


class UserProfileCreateSerializer(serializers.ModelSerializer):
    oauth = AuthCreateSerializer()
    trainee = TraineeProfileSerializer(read_only=False)
    trainer = TrainerProfileSerializer(read_only=False)

    class Meta:
        model = UserProfile
        fields = ['email', 'oauth', 'username', 'nickname', 'gender', 'birth_year', 'user_type', 'trainee', 'trainer']

    def create(self, validated_data):
        # 1. oauth정보의 유효성을 검증한 뒤, create action을 수행하는 serializer를 호출
        oauth = validated_data.pop('oauth')
        auth_serializer = AuthCreateSerializer(data=oauth)
        auth_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            auth_obj = auth_serializer.save()

            # 2. UserProfile 객체 생성
            user, created = UserProfile.objects.update_or_create(
                email=validated_data.pop('email'),
                defaults={
                    'oauth': auth_obj,
                    'username': validated_data.pop('username'),
                    'nickname': validated_data.pop('nickname'),
                    'gender': validated_data.pop('gender'),
                    'birth_year': validated_data.pop('birth_year'),
                    'user_type': validated_data.pop('user_type')
                }
            )
            if not created:
                raise serializers.ValidationError('user with this email addr already exists')

            # 3. user_type에 따라 TraineeProfile/TrainerProfile serialize화, 객체 생성
            user_info = validated_data.pop(user.user_type)
            if user.user_type == 'trainee':
                trainee_serializer = TraineeProfileCreateSerializer(data=user_info, partial=True)
                trainee_serializer.is_valid(raise_exception=True)
                trainee_obj, pk = trainee_serializer.save()
                user.trainee = trainee_obj
            else:
                trainer_serializer = TrainerProfileCreateSerializer(data=user_info, partial=True)
                trainer_serializer.is_valid(raise_exception=True)
                trainer_obj, pk = trainer_serializer.save()
                user.trainer = trainer_obj
            user.save()

            return user, user.pk
