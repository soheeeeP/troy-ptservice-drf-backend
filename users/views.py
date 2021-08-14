import json

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .services import GoogleAuthService, authenticate_provider
from .serializer import AuthSerializer


# authCode 및 tokenId 권한인증(GET)
class AuthView(generics.RetrieveAPIView):
    serializer_class = AuthSerializer

    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        auth_serializer = self.serializer_class(data=data)
        auth_serializer.is_valid(raise_exception=True)
        auth_serialized_data = auth_serializer.data

        provider_validation = authenticate_provider(provider=auth_serialized_data['provider'])
        if provider_validation:
            return Response({'message': 'invalid provider'}, status=status.HTTP_400_BAD_REQUEST)

        auth_service = GoogleAuthService()
        user_validation = auth_service.google_validate_email(data=auth_serialized_data)
        # user_validation = auth_service.google_validate_client_id(data=auth_serialized_data)
        if user_validation is not True:
            return Response({'message': 'invalid user'}, status=status.HTTP_400_BAD_REQUEST)

        # get_or_create_user
        # Userprofile.objects.filter(oauth_id=data['token_id']).exists()
        # return login user
        # else get additional info and register user
        pass


# 로그인 및 회원가입(POST), 회원정보수정(PUT/PATCH), 회원탈퇴(DELETE)
class UserView(generics.RetrieveUpdateDestroyAPIView):
    pass
