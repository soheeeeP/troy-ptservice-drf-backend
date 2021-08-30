import json

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import UserService
from .serializer import (
    LoginSerializer, UserProfileCreateSerializer
)


class LoginView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer

    # Login Request
    # header    : Authorization: 'Bearer [access_token]'
    # body      : {'email' : [email]}

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        response = {}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 로그인 및 회원가입(POST), 회원정보수정(PUT/PATCH), 회원탈퇴(DELETE)
class SignUpView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserProfileCreateSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_service = UserService(data=data)
        user_dict = user_service.set_user_profile_info()
        user_serializer = UserProfileCreateSerializer(
            # set_user_profile_info()는 UserProfile 객체 생성에 필요한 정보를 담은 dict를 return
            data=user_dict, partial=True
        )
        user_serializer.is_valid(raise_exception=True)
        user_obj, pk = user_serializer.save()

        # 로그인을 수행하고, token을 발급
        login_serializer = LoginSerializer(data={'email': data['base_info']['email']})
        login_serializer.is_valid(raise_exception=True)

        # user_pk와 발급된 token 정보를 담아서 응답 data를 구성
        response = {
            'user_pk': pk,
            'user_type': user_obj.user_type,
            'token': login_serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
