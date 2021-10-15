import json
from random import randint

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.db.models import Q

from rest_framework import generics, status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from utils.responses import OAuthErrorCollection as error_collection

from apps.oauth.models import Auth, AuthSMS
from api.oauth.services import AuthService, AuthSMSService, GoogleService
from api.oauth.serializer import AuthDefaultSerializer, AuthSMSCreateUpdateSerializer


# access_token 및 id_token 권한인증(GET)
class AuthView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = AuthDefaultSerializer
    authentication_classes = []
    queryset = Auth.objects.all()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
            self.queryset.get(
                Q(oauth_type=data['provider']),
                Q(oauth_token__exact=data['oauth_token'])
            )
            self.response['new_user'] = False
            return Response(self.response, status=status.HTTP_403_FORBIDDEN)
        except Auth.DoesNotExist:
            pass

        auth_serializer = self.serializer_class(data=data)
        auth_serializer.is_valid(raise_exception=True)
        auth_serialized_data = auth_serializer.data
        print(auth_serialized_data)

        provider_validation = AuthService(data=None).authenticate_provider(provider=auth_serialized_data['provider'])
        if provider_validation is False:
            self.response['validation']['provider'] = False
            return Response(self.response, status=status.HTTP_401_UNAUTHORIZED)

        auth_service = GoogleService()
        user_validation = auth_service.google_validate_client_id(data=auth_serialized_data)
        if user_validation is False:
            self.response['validation']['id_token'] = False
            return Response(self.response, status=status.HTTP_401_UNAUTHORIZED)

        return Response(self.response, status=status.HTTP_200_OK)


class AuthSMSView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = AuthSMSCreateUpdateSerializer

    success_response = openapi.Response(
        'OAUTH_200_SMS_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='휴대폰 인증을 위한 문자를 발송합니다.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='휴대폰 번호(11자리 숫자를 입력해주세요)'),
            }
        ),
        responses={
            200: success_response
        }
    )
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        data['auth_number'] = str(randint(1000, 10000))     # 4자리수 인증번호 생성

        sms_serializer = self.serializer_class(data=data)
        sms_serializer.is_valid(raise_exception=True)

        sms_service = AuthSMSService()
        result = sms_service.send_sms(phone_number=data['phone_number'], auth_number=data['auth_number'])
        if result is not True:
            raise ValidationError('문자 발송 간 오류가 발생했습니다.')

        sms_serializer.save()
        response = {
            'sms': sms_serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)


class AuthSMSValidateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = AuthSMSCreateUpdateSerializer

    success_response = openapi.Response(
        'OAUTH_200_SMS_SUCCESS_RESPONSE',
        schema=serializer_class
    )

    @swagger_auto_schema(
        operation_description='휴대폰 인증을 수행합니다.',
        responses={
            200: success_response
        }
    )
    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            sms = AuthSMS.objects.get(phone_number=data['phone_number'], auth_number=data['auth_number'])
        except AuthSMS.DoesNotExist:
            raise ValidationError('인증 객체가 존재하지 않습니다.')
        sms_serializer = self.serializer_class(instance=sms)
        sms_serializer.update(instance=sms, validated_data=data)

        response = {
            'sms': sms_serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
