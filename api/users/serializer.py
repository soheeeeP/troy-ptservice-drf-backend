import typing
from datetime import date, timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import transaction
from django.contrib.auth.models import update_last_login
from django.db.models.query import QuerySet

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import UserProfile, TraineeProfile, CoachProfile, BodyInfo

from apps.oauth.models import Auth
from apps.centers.models import Center
from api.centers.serializer import CenterSerializer
from api.oauth.serializer import AuthCreateSerializer
from api.tags.serializer import HashTagSerializer, HashTagCreateSerializer
from api.programs.serializer import EvaluationSerializer

from Troy.settings import base
from utils.authentication import TroyJWTAUthentication


class JWTSerializer(serializers.Serializer):
    token = serializers.SerializerMethodField()
    user_by_token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(user: UserProfile) -> typing.Optional[dict]:
        if base.SIMPLE_JWT['UPDATE_LAST_LOGIN'] is True:
            update_last_login(None, user)

        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return token

    @staticmethod
    def get_user_by_token(header: str) -> typing.Optional[UserProfile]:
        jwt_auth = TroyJWTAUthentication()
        user, validated_token = jwt_auth.authenticate(header=header)
        if user is None:
            raise serializers.ValidationError('invalid login credentials')
        return user


class BodyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyInfo
        fields = '__all__'

    def validate(self, attrs):
        return dict(attrs)


class BodyInfoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyInfo
        fields = '__all__'

    def create(self, validated_data):
        return BodyInfo.objects.create(**validated_data)


class TraineeProfileDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraineeProfile
        fields = ['id']


class TraineeSubProfileSerializer(serializers.Serializer):
    purpose = HashTagSerializer(many=True)
    body_info = serializers.SerializerMethodField()

    @staticmethod
    def get_body_info(obj: TraineeProfile) -> typing.Optional[BodyInfoSerializer]:
        body_info = BodyInfo.objects.filter(trainee_profile=obj).latest('created_at')
        return BodyInfoSerializer(instance=body_info).data


class TraineeProfileCreateUpdateSerializer(serializers.ModelSerializer):
    body_info = BodyInfoCreateSerializer(read_only=False)
    purpose = HashTagSerializer(many=True, read_only=False)

    class Meta:
        model = TraineeProfile
        fields = '__all__'

    def create(self, validated_data):
        tags_obj = HashTagCreateSerializer().bulk_create_tags_list(tags=validated_data.pop('purpose'))
        trainee = TraineeProfile.objects.create()
        trainee.purpose.add(*tags_obj)
        trainee.save()

        body_info_dict = validated_data.pop('body_info')
        BodyInfo.objects.create(trainee=trainee, **body_info_dict)

        return trainee, trainee.pk

    def update(self, instance, validated_data):
        tags_obj = HashTagCreateSerializer().bulk_create_tags_list(tags=validated_data.pop('purpose', None))
        if tags_obj:
            instance.purpose.all().delete()
            instance.purpose.add(*tags_obj)
            instance.save()

        body_info_dict = validated_data.pop('body_info', None)
        if body_info_dict:
            BodyInfo.objects.create(trainee=instance, **body_info_dict)

        return instance, instance.pk


class CoachProfileDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachProfile
        fields = ['id']


class CoachSubProfileSerializer(serializers.ModelSerializer):
    specialty = HashTagSerializer(many=True, read_only=False)
    center = CenterSerializer(read_only=False)

    class Meta:
        model = CoachProfile
        fields = ['specialty', 'years_career', 'license', 'education', 'center']


class CoachListSerializer(serializers.Serializer):
    coach_list = serializers.SerializerMethodField()

    @staticmethod
    def get_coach_list(queryset: QuerySet) -> typing.Optional[list]:
        coach_list = list()
        for q in queryset.iterator():
            coach = dict()
            coach['id'] = q.userprofile.id
            coach['nickname'] = q.userprofile.nickname
            coach['profile_img'] = q.userprofile.profile_img.url if q.userprofile.profile_img else None
            coach['specialty'] = list(q.specialty.values_list('tag_content', flat=True).all())
            coach['center'] = CenterSerializer(instance=q.center).data
            coach['evaluation'] = EvaluationSerializer().get_coach_evaluation(obj=q)
            coach_list.append(coach)
        return coach_list


class CoachProfileCreateUpdateSerializer(serializers.ModelSerializer):
    center = CenterSerializer(read_only=False)
    specialty = HashTagSerializer(many=True, read_only=False)

    class Meta:
        model = CoachProfile
        fields = '__all__'
        list_serializer_class = CoachListSerializer

    def create(self, validated_data):
        center = validated_data.pop('center')
        center_obj = Center.objects.create(**center)
        tags_obj = HashTagCreateSerializer().bulk_create_tags_list(tags=validated_data.pop('specialty'))

        coach = CoachProfile.objects.create(center=center_obj)
        coach.specialty.add(*tags_obj)
        coach.save()

        return coach, coach.pk

    def update(self, instance, validated_data):
        center = validated_data.pop('center', None)
        if center:
            instance.center = Center.objects.create(**center)

        tags_obj = HashTagCreateSerializer().bulk_create_tags_list(tags=validated_data.pop('specialty', None))
        if tags_obj:
            instance.specialty.all().delete()
            instance.specialty.add(*tags_obj)

        instance.save()
        return instance, instance.pk


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'nickname', 'gender', 'birth', 'profile_img', 'user_type']

    def validate(self, attrs):
        super(UserProfileSerializer, self).validate(attrs)


class UserProfileCreateUpdateSerializer(serializers.Serializer):
    oauth = AuthCreateSerializer(
        help_text='회원가입 시 필수로 입력해야 하는 oauth 정보로 프로필 업데이트 시에는 요구되지 않습니다.'
    )
    email = serializers.EmailField(
        max_length=255,
        help_text='회원가입/프로필 업데이트 시에 필수로 요구되는 값입니다.'
    )
    username = serializers.CharField(max_length=150, allow_blank=True, allow_null=True, required=False)
    nickname = serializers.CharField(max_length=150, allow_blank=True, allow_null=True, required=False)
    gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES, allow_blank=True, allow_null=True, required=False)
    birth = serializers.DateField(
        validators=[
            MinValueValidator(limit_value=date(1984, 1, 1)),
            MaxValueValidator(limit_value=date.today() - timedelta(days=1))
        ],
        allow_null=True,
        required=False
    )
    profile_img = serializers.FileField(required=False, allow_null=True)
    user_type = serializers.ChoiceField(
        choices=UserProfile.USER_CHOICES,
        help_text='회원가입/프로필 업데이트 시에 필수로 요구되는 사용자 타입(trainee/coach) 값입니다.'
    )
    trainee = TraineeProfileCreateUpdateSerializer(
        read_only=False, required=False,
        help_text='회원가입/프로필 업데이트 시에 사용자 타입에 따라 선택적으로 요구되는 값입니다.'
    )
    coach = CoachProfileCreateUpdateSerializer(
        read_only=False, required=False,
        help_text='회원가입/프로필 업데이트 시에 사용자 타입에 따라 선택적으로 요구되는 값입니다.'
    )

    class Meta:
        model = UserProfile

    def validate_oauth(self, value):
        try:
            oauth = Auth.objects.get(oauth_token__exact=value['oauth_token'])
            raise serializers.ValidationError('this oauth-token already exists')
        except Auth.DoesNotExist:
            return value

    def validate_nickname(self, value):
        try:
            self.Meta.model.objects.get(nickname=value)
            raise serializers.ValidationError('this nickname already exists')
        except self.Meta.model.DoesNotExist:
            return value

    @staticmethod
    def create_update_sub_profile(instance: typing.Optional[UserProfile], user_type, data):
        if user_type == UserProfile.USER_CHOICES.trainee:
            serializer = TraineeProfileCreateUpdateSerializer(instance=instance, data=data, partial=True)
        else:
            serializer = CoachProfileCreateUpdateSerializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj, pk = serializer.save()
        return obj

    def create(self, validated_data):
        oauth = validated_data.pop('oauth')
        auth_serializer = AuthCreateSerializer(data=oauth)
        auth_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            auth_obj = auth_serializer.save()
            user = UserProfile.objects.create(
                oauth=auth_obj,
                email=validated_data.pop('email'),
                username=validated_data.pop('username'),
                nickname=validated_data.pop('nickname'),
                gender=validated_data.pop('gender'),
                birth=validated_data.pop('birth'),
                user_type=validated_data.pop('user_type'),
                profile_img=validated_data.pop('profile_img', None)
            )
            user_type = user.user_type
            trainee_coach_profile = self.create_update_sub_profile(
                instance=None,
                user_type=user_type,
                data=validated_data.pop(user_type)
            )
            if user_type == UserProfile.USER_CHOICES.trainee:
                user.trainee = trainee_coach_profile
            else:
                user.coach = trainee_coach_profile
            user.save()
            return user, user.pk

    def update(self, instance, validated_data):

        sid = transaction.savepoint()
        try:
            UserProfile.objects.update(
                email=validated_data.pop('email', instance.email),
                username=validated_data.pop('username', instance.username),
                nickname=validated_data.pop('nickname', instance.nickname),
                gender=validated_data.pop('gender', instance.gender),
                birth=validated_data.pop('birth', instance.birth),
                profile_img=validated_data.pop('profile_img', instance.profile_img)
            )
        except ValidationError:
            transaction.savepoint_rollback(sid)
            raise ValidationError('validation err while updating UserProfile')

        user_type = instance.user_type
        if user_type == UserProfile.USER_CHOICES.trainee:
            instance = instance.trainee
        else:
            instance = instance.coach

        profile_info = validated_data.pop(user_type, None)
        if profile_info:
            self.create_update_sub_profile(
                instance=instance,
                user_type=user_type,
                data=profile_info
            )
        return instance, instance.pk


class LoginSignUpResponseSerializer(serializers.Serializer):
    token = JWTSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)
    trainee = TraineeProfileDefaultSerializer(read_only=True)
    coach = CoachProfileDefaultSerializer(read_only=True)
