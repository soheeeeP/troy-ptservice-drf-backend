import os, requests
from datetime import datetime

from apps.users.models import UserProfile
from api.users.serializer import (
    JWTSerializer, UserProfileSerializer, CoachProfileDefaultSerializer, TraineeProfileDefaultSerializer
)

from Troy.settings import base


class UserService(object):
    @staticmethod
    def set_user_profile_info(data, img):
        user_profile = data
        if 'birth' in data:
            user_profile['birth'] = datetime.strptime(data['birth'], '%Y-%m-%d').date()
        user_profile['profile_img'] = img
        return data

    @staticmethod
    def set_login_signup_response_info(user: UserProfile, user_type: str, **kwargs):
        response = dict()

        response['token'] = JWTSerializer().get_token(user=user)
        response['user'] = UserProfileSerializer(instance=user).data
        if user.is_staff:
            response['user']['user_type'] = 'superuser'
            return response

        response['user']['user_type'] = user_type
        if user_type == UserProfile.USER_CHOICES.coach:
            response[user_type] = CoachProfileDefaultSerializer(instance=user.coach).data
        else:
            response[user_type] = TraineeProfileDefaultSerializer(instance=user.trainee).data
        return response
