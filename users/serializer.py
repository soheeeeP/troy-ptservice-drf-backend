from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, TraineeProfile, TrainerProfile
from Troy.settings import base
from Troy.backend import PasswordlessBackend


class AuthSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google', 'kakao', 'naver'])
    id_token = serializers.CharField()
    access_token = serializers.CharField()
    oauth = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()

    def validate(self, attrs):
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'])
        print(user)
        if user is None:
            raise serializers.ValidationError('invalid login credentials')

        refresh = RefreshToken.for_user(user)
        data = super().validate(attrs)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        print(data)

        if base.SIMPLE_JWT['UPDATE_LAST_LOGIN'] is True:
            update_last_login(None, user)

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
