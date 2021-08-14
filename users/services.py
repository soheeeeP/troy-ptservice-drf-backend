import requests

from rest_framework.exceptions import ValidationError

from Troy.settings import base


def authenticate_provider(provider):
    print(provider)
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

    # data = {
    #     'provider': '[idpId]',
    #     'id_token': '[tokenObj][id_token]',
    #     'access_token': '[tokenObj][access_token]',
    #     'oauth': '[googleId]',
    #     'email': '[profileObj][email]',
    #     'username': '[profileObj][name]',
    #     'profile_img': '[profileObj][imageUrl]'
    # }

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

    def obtain_token(self):
        pass

    def refresh_token(self):
        pass

    def verify_token(self):
        pass


class UserService(object):
    # email로 user unique check
    # def email_duplicate_check()
        # user_Create할때 passwd 저장안함!!!!
        # 아니면 access_token으로 make_password

    # email 추가정보 입력
    # def register_additional_info_using_email()

    # token이 없음 -> validate -> signup -> additional_info -> generate token -> front로 login정보와 token을 보
    pass
