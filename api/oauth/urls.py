from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.oauth.views import *

app_name = 'oauth'
urlpatterns = [
    path('validate', AuthView.as_view(), name='validate'),
    path('token/obtain', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # 휴대폰 인증번호 발송 및 인증 URL
    path('sms', AuthSMSView.as_view(), {"action": "POST"}, name='sms'),
    path('sms/validate', AuthSMSValidateView.as_view(), {"action": "PATCH"}, name='sms_validate'),
]
