from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import AuthView, UserView

app_name = 'users'
urlpatterns = [
    path('login/validate',AuthView.as_view(), name='login_validate'),
    path('signup/',UserView.as_view(),name='signup'),
    # tokenID를 사용하여 user를 get_or_create. login한 상태로 Response전
    # path('token/login', TokenObtainPairView.as_view(), name='login'),
    # google callback server에서 유효한 user인지 확인, access_token return
    # path('token/validate',)
    # jwt를 받아 token을 검증하여 상태코드로 반환
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    # jwt를 받아 token을 검증하여 새로운 토큰(refresh_token) 반환
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')

]