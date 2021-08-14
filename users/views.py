import json

from django.urls import reverse
from django.views.generic import RedirectView

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile, TrainerProfile, TraineeProfile
from .services import GoogleAuthService, authenticate_provider
from .serializer import AuthSerializer, UserProfileSerializer


# access_token 및 id_token 권한인증(GET)
class AuthView(RedirectView, generics.RetrieveAPIView):
    serializer_class = AuthSerializer
    pattern_name = 'users:signup'

    def get_redirect_url(self, *args, **kwargs):
        context = kwargs.pop('user_profile')
        print(f'user info : {context}')
        return reverse(self.pattern_name, kwargs=context)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        auth_serializer = self.serializer_class(data=data)
        auth_serializer.is_valid(raise_exception=True)
        auth_serialized_data = auth_serializer.data
        print(auth_serialized_data)
        provider_validation = authenticate_provider(provider=auth_serialized_data['provider'])
        if provider_validation is False:
            return Response({'message': 'invalid provider'})
        # print('google provider validation succeed')

        auth_service = GoogleAuthService()
        user_validation = auth_service.google_validate_email(data=auth_serialized_data)
        # user_validation = auth_service.google_validate_client_id(data=auth_serialized_data)
        # print(f'user validation RETURN VALUE {user_validation}')
        if user_validation is False:
            return Response({'message': 'invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        print('google user validation succeed')

        try:
            user = UserProfile.objects.get(email=data['email'])
            return Response({'message': 'email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            url = self.get_redirect_url(user_profile=data)
            # print(f'redirect to : {url}')
            return super(AuthView, self).get()


# 로그인 및 회원가입(POST), 회원정보수정(PUT/PATCH), 회원탈퇴(DELETE)
class UserView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


