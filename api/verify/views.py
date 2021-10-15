from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.models import UserProfile, CoachProfile

from utils.responses import VerifyErrorCollection as error_collection
from utils.swagger import VerifyParamCollection as verify_param_collection


class NicknameVerifyView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()

    success_response = openapi.Response(
        'VERIFY_200_NICKNAME_SUCCESS_RESPONSE',
        examples={
            'application/json': {
                'nickname': 'bool'
            }
        }
    )

    @swagger_auto_schema(
        manual_parameters=[
            verify_param_collection.nickname,
        ],
        operation_description='사용자 닉네임 중복여부를 확인합니다.',
        responses={
            200: success_response,
            400:
                error_collection.VERIFY_400_NICKNAME_DUPLICATE_CHECK_VALIDATION_ERROR.as_md() +
                error_collection.VERIFY_400_NICKNAME_DUPLICATE_CHECK_PARAMETER_ERROR.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        nickname = request.GET.get('q', None)
        if nickname:
            try:
                self.queryset.get(nickname__iexact=nickname)
                raise ValidationError('이미 사용중인 닉네임입니다.')
            except UserProfile.DoesNotExist:
                response = {'nickname': True}
                return Response(response, status=status.HTTP_200_OK)

        raise ValidationError('중복 확인을 수행할 data 종류를 parameter로 전달해주세요')


class CoachCodeVerifyView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()

    success_response = openapi.Response(
        'VERIFY_200_COACHCODE_SUCCESS_RESPONSE',
        examples={
            'application/json': {
                'coachcode': 'bool'
            }
        }
    )

    @swagger_auto_schema(
        manual_parameters=[
            verify_param_collection.coach_code,
        ],
        operation_description='코치 인증 코드가 유효한지 확인합니다.',
        responses={
            200: success_response,
            400:
                error_collection.VERIFY_400_COACHCODE_EXIST_CHECK_VALIDATION_ERROR.as_md() +
                error_collection.VERIFY_400_COACHCODE_EXIST_CHECK_PARAMETER_ERROR.as_md()
        }
    )
    def get(self, request, *args, **kwargs):
        coach_code = request.GET.get('q', None)
        if coach_code:
            try:
                self.queryset.get(oauth__oauth_token=coach_code)
            except UserProfile.DoesNotExist:
                raise ValidationError('존재하지 않는 코치 코드입니다.')

            response = {'coachcode': True}
            return Response(response, status=status.HTTP_200_OK)

        raise ValidationError('코치 인증 코드를 parameter로 전달해주세요.')
