import json
import os, requests

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from Troy.settings import base


def user_login_from_authview(user: UserProfile):
    response = requests.post('users:login', data={'email': user.email})
    response_code = response.getcode()
    login_data = json.loads(response.read().decode('utf-8'))

    if response_code == 201:
        return Response({'newUser': False, 'login': {'message': 'success', 'user': user.pk}}, status=response_code)
    else:
        return Response({'newUser': False, 'login': {'message': 'fail'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def authenticate_provider(provider):
    # print(provider)
    # social login 확장 고려하여 provider 구분
    if provider == 'google':
        return True
    else:
        return False


class GoogleAuthService(object):
    def __init__(self):
        self.base_url = 'http://localhost:8000/'
        self.redirect_uri = self.base_url + 'accounts/google/callback'
        self.google_id_token_info_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
        self.google_email_info_url = 'https://www.googleapis.com/oauth2/v1/tokeninfo'

    def google_validate_email(self, data):
        # [access_token]으로 Google OAuth에 request 전송
        # email로 user 유효성 검증 (email은 unique한 값을 가진다는 성질을 이용한 logic)
        context = {
            'access_token': data['access_token']
        }
        response = requests.post(self.google_email_info_url, data=context)
        if not response.ok:
            raise ValidationError(response.reason)

        response_json = response.json()
        user_email = data['email']
        # print(f'email validation succeed by {user_email}')

        response_flag = [user_email == response_json['email']]
        # print(user_email)
        # print(response_json['email'])
        # print(f'response flag is {response_flag}')
        return response_flag

    def google_validate_client_id(self, data):
        # [id_token]으로 Google OAuth에 request 전송
        # client_id값으로 user 유효성 검증 (request를 보낸 client가 우리의 client가 맞는지 확인하는 logic)
        context = {
            'id_token': data['id_token']
        }
        response = requests.post(self.google_id_token_info_url, data=context)
        if not response.ok:
            raise ValidationError(response.reason)

        response_json = response.json()
        google = getattr(base, 'auth')['google']
        client_id = google['client_id']

        response_flag = [client_id == response_json['aud']]
        return response_flag


class UserService(object):
    def __init__(self, data):
        self.oauth_info = data['oauth_info']
        self.sub_info = data['sub_info']
        self.user_type = data['user_type']

    def set_user_profile_info(self, **kwargs):
        user = UserProfile(
            email=self.oauth_info['email'],
            username=self.oauth_info['username'],
            oauth_type=self.oauth_info['oauth_type'],
            oauth_token=self.oauth_info['oauth_token'],
            # profile_img=self.save_img_from_url(
            #     img_id=oauth_info['oauth_token'],
            #     url=oauth_info['profile_img']
            # ),
            gender=self.sub_info['gender'],
            birth_year=self.sub_info['birth_year'],
            nickname=self.sub_info['nickname'],
            user_type=self.user_type
        )
        return user

    @staticmethod
    def save_img_from_url(self, img_id, url):
        ext = '.png'
        img_data = requests.get(url).content
        img_path = os.path.join(base.MEDIA_ROOT, 'profile', img_id+ext)
        with open(img_path, 'wb') as f:
            file = f.write(img_data)

        return img_data
