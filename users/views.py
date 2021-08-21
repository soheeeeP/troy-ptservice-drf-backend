import json

from django.db.models import Q
from django.urls import reverse
from django.views.generic import RedirectView

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile, TrainerProfile, TraineeProfile
from .services import (
    authenticate_provider, user_login_from_authview,
    GoogleAuthService
)
from .serializer import AuthSerializer, LoginSerializer, UserProfileSerializer


# access_token 및 id_token 권한인증(GET)
class AuthView(RedirectView, generics.RetrieveAPIView):
    serializer_class = AuthSerializer

    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        response = {'validation': {}, 'user': {}}

        auth_serializer = self.serializer_class(data=data)
        auth_serializer.is_valid(raise_exception=True)
        auth_serialized_data = auth_serializer.data

        provider_validation = authenticate_provider(provider=auth_serialized_data['provider'])
        if provider_validation is False:
            return Response({'invalidProvider': False}, status=status.HTTP_400_BAD_REQUEST)
        response['validation']['provider'] = 'success'

        auth_service = GoogleAuthService()
        user_validation = auth_service.google_validate_email(data=auth_serialized_data)
        if user_validation is False:
            return Response({'invalidUser': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response['validation']['email'] = 'success'

        response['user']['info'] = auth_serialized_data
        try:
            user = UserProfile.objects.get(
                Q(oauth_type=data['provider']),
                Q(oauth_token=data['oauth'])
            )
            return user_login_from_authview(user=user)
        except UserProfile.DoesNotExist:
            response['user']['status'] = 'new'
            return Response(response, status=status.HTTP_200_OK)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (IsAuthenticated,)

    # Login Request
    # header    : Authorization: 'Bearer [access_token]'
    # body      : {'email' : [email]}

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 로그인 및 회원가입(POST), 회원정보수정(PUT/PATCH), 회원탈퇴(DELETE)
class UserView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer

    def __init__(self):
        pass

    def create(self, request, context=None, *args, **kwargs):
        print(kwargs.pop('email'))
        request.GET.get('email')
        pass

    def update(self, request, *args, **kwargs):
        # pk로 object열고, 검증한뒤에 update
        pass

    def destroy(self, request, *args, **kwargs):
        pass


