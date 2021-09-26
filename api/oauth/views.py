import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.db.models import Q

from rest_framework import generics, status, mixins
from rest_framework.response import Response

from utils.responses import OAuthErrorCollection as error_collection

from apps.oauth.models import Auth
from api.oauth.services import AuthService, GoogleService
from api.oauth.serializer import AuthDefaultSerializer

from apps.users.models import UserProfile


# access_token 및 id_token 권한인증(GET)
class AuthView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = AuthDefaultSerializer

    def __init__(self):
        self.response = {
            'validation': {
                'provider': True,
                'id_token': True
            },
            'new_user': True
        }

    success_response = openapi.Response(
        'OAUTH_200_SUCCESS_RESPONSE',
        examples={
            'application/json': {
                'validation':
                    {
                        'provider': 'bool',
                        'id_token': 'bool'
                    },
                'new_user': 'bool'
            }
        }
    )

    @swagger_auto_schema(
        operation_description='oauth validation 수행하기',
        responses={
            200: success_response,
            401:
                error_collection.OAUTH_401_PROVIDER_INVALID.as_md() +
                error_collection.OAUTH_401_ID_TOKEN_INVALID.as_md(),
            403:
                error_collection.OAUTH_403_USER_ALREADY_EXISTS.as_md()
        }
    )
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        try:
            Auth.objects.get(
                Q(oauth_type=data['provider']),
                Q(oauth_token=data['oauth_token'])
            )
            self.response['new_user'] = False
            return Response(self.response, status=status.HTTP_403_FORBIDDEN)
        except Auth.DoesNotExist:
            pass

        auth_serializer = self.serializer_class(data=data)
        auth_serializer.is_valid(raise_exception=True)
        auth_serialized_data = auth_serializer.data

        provider_validation = AuthService(data=None).authenticate_provider(provider=auth_serialized_data['provider'])
        if provider_validation is False:
            self.response['validation']['provider'] = False
            return Response(self.response, status=status.HTTP_401_UNAUTHORIZED)

        auth_service = GoogleService()
        user_validation = auth_service.google_validate_client_id(data=auth_serialized_data)
        if user_validation is False:
            self.response['validation']['id_token'] = False

        return Response(self.response, status=status.HTTP_401_UNAUTHORIZED)
