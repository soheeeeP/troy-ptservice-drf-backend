import os, requests
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.db import transaction

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, TraineeProfile, TrainerProfile, BodyInfo
from tags.serializer import HashTagSerializer
from centers.serializer import CenterSerializer
from Troy.settings import base


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
    # profile_img = serializers.FileField(max_length=None)

    class Meta:
        model = UserProfile
        fields = ['email', 'oauth_type', 'oauth_token', 'username', 'nickname', 'gender', 'birth_year']

    def create(self, validated_data):
        user, created = UserProfile.objects.update_or_create(
            email=validated_data.get('email', None),
            defaults={
                'oauth_type': validated_data.get('oauth_type', None),
                'oauth_token': validated_data.get('oauth_token', None),
                'username': validated_data.get('username', None),
                'nickname': validated_data.get('nickname', None),
                'gender': validated_data.get('gender', None),
                'birth_year': validated_data.get('birth_year', None)
            }
        )
        return user


class BodyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyInfo
        fields = '__all__'

    def create(self, validated_data):
        return super(BodyInfoSerializer, self).create(validated_data)


class TrainerProfileSerializer(serializers.ModelSerializer):
    center = CenterSerializer(read_only=True)

    class Meta:
        model = TrainerProfile
        fields = ['center', 'years_career', 'license', 'education']

    def create(self, validated_data):
        return super(TrainerProfileSerializer, self).create(validated_data)