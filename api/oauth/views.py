import json

from django.db.models import Q

from rest_framework import generics, status
from rest_framework.response import Response

from apps.oauth.models import Auth
from api.oauth.services import GoogleAuthService
from api.oauth.serializer import AuthDefaultSerializer

from apps.users.models import UserProfile


# access_token 및 id_token 권한인증(GET)
class AuthView(generics.RetrieveAPIView):
    serializer_class = AuthDefaultSerializer

    def retrieve(self, request, *args, **kwargs):
        data = json.loads(request.body)
        response = {'validation': {}, 'user': {}}

        auth_serializer = self.serializer_class(data=data)
        auth_serializer.is_valid(raise_exception=True)
        auth_serialized_data = auth_serializer.data

        auth_service = GoogleAuthService()
        provider_validation = auth_service.authenticate_provider(provider=auth_serialized_data['provider'])
        if provider_validation is False:
            return Response({'invalidProvider': False}, status=status.HTTP_401_UNAUTHORIZED)
        response['validation']['provider'] = 'success'

        user_validation = auth_service.google_validate_client_id(data=auth_serialized_data)
        if user_validation is False:
            return Response({'invalidUser': False}, status=status.HTTP_401_UNAUTHORIZED)
        response['validation']['email'] = 'success'

        response['user']['info'] = auth_serialized_data
        try:
            oauth = Auth.objects.get(
                Q(oauth_type=data['provider']),
                Q(oauth_token=data['oauth'])
            )
            user = UserProfile.objects.get(oauth=oauth)
            return Response({'newUser': False}, status=status.HTTP_403_FORBIDDEN)
        except Auth.DoesNotExist:
            response['user']['status'] = 'new'
            return Response(response, status=status.HTTP_200_OK)
