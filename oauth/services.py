import json
import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Auth

from users.models import UserProfile
from Troy.settings import base


class GoogleAuthService(object):
    def __init__(self):
        self.google_id_token_info_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
        self.google_email_info_url = 'https://www.googleapis.com/oauth2/v1/tokeninfo'

    @staticmethod
    def authenticate_provider(provider):
        # print(provider)
        # social login 확장 고려하여 provider 구분
        if provider == 'google':
            return True
        else:
            return False

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


class AuthService(object):
    def __init__(self, data):
        self.oauth = data

    def sef_auth_info(self, **kwargs):
        auth = Auth(
            oauth_type=self.oauth['oauth_type'],
            oauth_token=self.oauth['oauth_token']
        )
        return auth
