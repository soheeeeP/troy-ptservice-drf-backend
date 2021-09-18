import typing

from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import UserProfile, TraineeProfile, CoachProfile, BodyInfo

from apps.centers.models import Center
from api.centers.serializer import CenterSerializer
from api.oauth.serializer import AuthCreateSerializer
from api.programs.serializer import ProgramDetailSerializer
from apps.tags.models import HashTag
from api.tags.serializer import HashTagSerializer

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


class UserProfileDefaultSerializer(ProgramDetailSerializer, serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'nickname', 'gender', 'birth_year', 'profile_img']

    def validate(self, attrs):
        super(UserProfileDefaultSerializer, self).validate(attrs)


class TraineeSubProfileSerializer(serializers.ModelSerializer):
    purpose = HashTagSerializer(many=True)
    body_info = serializers.SerializerMethodField()
    goal = serializers.SerializerMethodField()

    @staticmethod
    def get_body_info(obj: TraineeProfile) -> typing.Optional[BodyInfoSerializer]:
        if BodyInfo.objects.filter(trainee_profile=obj).exists() is not True:
            return None

        body_info = BodyInfo.objects.filter(trainee_profile=obj).latest('date')
        return BodyInfoSerializer(instance=body_info).data


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


class CoachSubProfileSerializer(serializers.ModelSerializer):
    specialty = HashTagSerializer(many=True, read_only=False)
    center = CenterSerializer(read_only=False)

    class Meta:
        model = CoachProfile
        fields = ['specialty', 'years_career', 'license', 'education', 'center']


class CoachProfileCreateSerializer(serializers.ModelSerializer):
    center = CenterSerializer(read_only=False)
    specialty = HashTagSerializer(many=True, read_only=False)

    class Meta:
        model = CoachProfile
        fields = '__all__'

    def create(self, validated_data):
        center = validated_data.pop('center')
        center_obj = Center.objects.create(**center)

        tags = validated_data.pop('specialty')
        tags_list = [HashTag(tag_type=x['tag_type'], tag_content=x['tag_content']) for x in tags]
        tags_obj = HashTag.objects.bulk_create(tags_list)
        for t in tags_obj:
            t.save()

        coach = CoachProfile.objects.create(center=center_obj)
        coach.specialty.add(*tags_obj)
        coach.save()

        return coach, coach.pk


class UserProfileCreateSerializer(serializers.ModelSerializer):
    oauth = AuthCreateSerializer()
    trainee = TraineeProfileCreateSerializer(read_only=False)
    coach = CoachProfileCreateSerializer(read_only=False)

    class Meta:
        model = UserProfile
        fields = ['email', 'oauth', 'username', 'nickname', 'gender', 'birth_year', 'user_type', 'trainee', 'coach']

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

            # 3. user_type에 따라 TraineeProfile/CoachProfile serialize화, 객체 생성
            user_info = validated_data.pop(user.user_type)
            if user.user_type == 'trainee':
                trainee_serializer = TraineeProfileCreateSerializer(data=user_info, partial=True)
                trainee_serializer.is_valid(raise_exception=True)
                trainee_obj, pk = trainee_serializer.save()
                user.trainee = trainee_obj
            else:
                coach_serializer = CoachProfileCreateSerializer(data=user_info, partial=True)
                coach_serializer.is_valid(raise_exception=True)
                coach_obj, pk = coach_serializer.save()
                user.coach = coach_obj
            user.save()

            return user, user.pk
