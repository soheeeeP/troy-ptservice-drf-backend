from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import AuthView, UserView

app_name = 'users'
urlpatterns = [
    path('login/validate', AuthView.as_view(), name='login_validate'),
    path('signup', UserView.as_view(), name='signup'),

    # 가입된 user에 대한 jwt 생성
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # token을 검증하여 상태코드로 반환
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    # refresh_token을 검증하여 새로운 access_token 반환
    path('token/refresh', TokenRefreshView.as_view(), name = 'token_refresh')

]