import json
import requests

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import UserProfile
from Troy.settings import base


def user_login_from_authview(user: UserProfile):
    response = requests.post('users:login', data={'email': user.email})
    response_code = response.getcode()
    login_data = json.loads(response.read().decode('utf-8'))

    if response_code == 201:
        return Response({'newUser': False, 'login': {'message': 'success', 'user': user.pk}},status=response_code)
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
    # email로 user unique check
    # def email_duplicate_check()
    # user_Create할때 passwd 저장안함!!!!
    # 아니면 access_token으로 make_password

    # email 추가정보 입력
    # def register_additional_info_using_email()

    # token이 없음 -> validate -> signup -> additional_info -> generate token -> front로 login정보와 token을 보
    pass
