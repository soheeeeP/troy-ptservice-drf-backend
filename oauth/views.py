import json

from django.db.models import Q

from rest_framework import generics, mixins, status
from rest_framework.response import Response

from .models import Auth
from .services import user_login_from_authview, GoogleAuthService
from .serializer import AuthDefaultSerializer

from users.models import UserProfile


# access_token 및 id_token 권한인증(GET)
class AuthView(generics.RetrieveAPIView):
    serializer_class = AuthDefaultSerializer

    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        response = {'validation': {}, 'user': {}}

        auth_serializer = self.serializer_class(data=data)
        auth_serializer.is_valid(raise_exception=True)
        auth_serialized_data = auth_serializer.data

        auth_service = GoogleAuthService()
        provider_validation = auth_service.authenticate_provider(provider=auth_serialized_data['provider'])
        if provider_validation is False:
            return Response({'invalidProvider': False}, status=status.HTTP_400_BAD_REQUEST)
        response['validation']['provider'] = 'success'

        user_validation = auth_service.google_validate_email(data=auth_serialized_data)
        if user_validation is False:
            return Response({'invalidUser': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response['validation']['email'] = 'success'

        response['user']['info'] = auth_serialized_data
        try:
            oauth = Auth.objects.get(
                Q(oauth_type=data['provider']),
                Q(oauth_token=data['oauth'])
            )
            user = UserProfile.objects.get(oauth=oauth)
            return user_login_from_authview(user=user)
        except Auth.DoesNotExist:
            response['user']['status'] = 'new'
            return Response(response, status=status.HTTP_200_OK)
