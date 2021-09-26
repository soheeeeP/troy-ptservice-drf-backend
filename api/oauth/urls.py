from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.oauth.views import AuthView

app_name = 'oauth'
urlpatterns = [
    path('validate', AuthView.as_view(), name='validate'),
    path('token/obtain', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]
