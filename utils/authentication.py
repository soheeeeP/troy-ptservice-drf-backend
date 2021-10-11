from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from Troy.settings.base import SIMPLE_JWT


class TroyJWTAUthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()
    @classmethod
    def get_user_id(cls, validated_token):
        try:
            return validated_token[SIMPLE_JWT.get('USER_ID_CLAIM')]
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

    def get_user(self, validated_token):
        user_id = self.get_user_id(validated_token=validated_token)
        try:
            user = self.user_model.objects\
                .select_related('trainee', 'coach')\
                .get(**{SIMPLE_JWT.get('USER_ID_FIELD'): user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(_('User is inactive'), code='user_inactive')

        return user

    def authenticate(self, header):
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
