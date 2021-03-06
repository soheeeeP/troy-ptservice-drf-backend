import base64
import hashlib
import hmac
import requests
import time
import json

from rest_framework.exceptions import ValidationError

from Troy.settings import base
from apps.oauth.models import Auth


class GoogleService(object):
    def __init__(self):
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

        response_flag = [user_email == response_json['email']]
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

    @staticmethod
    def authenticate_provider(provider):
        # social login 확장 고려하여 provider 구분
        if provider == 'google':
            return True
        else:
            return False

    def sef_auth_info(self, **kwargs):
        auth = Auth(
            oauth_type=self.oauth['oauth_type'],
            oauth_token=self.oauth['oauth_token']
        )
        return auth


class AuthSMSService(object):
    def __init__(self):
        self.sender = '01089099796'
        self.naver = getattr(base, 'auth')['naver']
        self.url = 'https://sens.apigw.ntruss.com'
        self.uri = f'/sms/v2/services/{self.naver["service_id"]}/messages'

    def make_signature(self, timestamp):
        secret_key = bytes(self.naver['secret_key'], 'UTF-8')

        message = "POST "+self.uri+"\n"+timestamp+"\n"+self.naver['access_key']
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

        return signingKey

    def send_sms(self, phone_number, auth_number):
        timestamp = str(int(time.time()*1000))
        context = {
            'type': 'SMS',
            'contentType': 'COMM',
            'countryCode': '82',
            'from': self.sender,
            'content': f'Troy 인증번호 [{auth_number}]를 입력해주세요.',
            'messages': [{
                'to': phone_number
            }]
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': self.naver['access_key'],
            'x-ncp-apigw-signature-v2': self.make_signature(timestamp=timestamp)
        }
        response = requests.post(self.url+self.uri, headers=headers, json=context)

        if not response.ok:
            raise ValidationError(response.reason)

        return True
