import os, requests


from apps.users.models import UserProfile
from api.users.serializer import (
    LoginSerializer,
    UserProfileSerializer, CoachProfileDefaultSerializer, TraineeProfileDefaultSerializer
)

from Troy.settings import base


class UserService(object):
    def __init__(self, data):
        self.oauth = data['oauth']
        self.base = data['base_info']
        self.sub = data['sub_info']
        self.user_type = data['user_type']
        self.user_type_info = data['user_type_info']

    def set_user_profile_info(self, **kwargs):
        user_dict = {
            'email': self.base['email'],
            'username': self.base['username'],
            'oauth': self.oauth,
            'gender': self.sub['gender'],
            'birth_year': self.sub['birth_year'],
            'nickname': self.sub['nickname'],
            'user_type': self.user_type,
            self.user_type: self.user_type_info,
        }
        return user_dict

    @staticmethod
    def set_login_signup_response_info(user: UserProfile, user_type: str, **kwargs):
        response = {
            'user': UserProfileSerializer(instance=user).data,
            'token': LoginSerializer().get_token(user=user),
        }
        if user_type == UserProfile.USER_CHOICES.coach:
            response[user_type] = CoachProfileDefaultSerializer(instance=user.coach).data
        else:
            response[user_type] = TraineeProfileDefaultSerializer(instance=user.trainee).data
        return response

    @staticmethod
    def save_img_from_url(self, img_id, url):
        ext = '.png'
        img_data = requests.get(url).content
        img_path = os.path.join(base.MEDIA_ROOT, 'profile', img_id + ext)
        with open(img_path, 'wb') as f:
            file = f.write(img_data)

        return img_data
