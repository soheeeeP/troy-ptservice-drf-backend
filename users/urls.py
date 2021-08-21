from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import AuthView, LoginView, UserView

app_name = 'users'
urlpatterns = [
    path('oauth/validate', AuthView.as_view(), name='validate'),
    path('signup/', UserView.as_view(), name='signup'),

    path('login', LoginView.as_view(), name='login'),
    path('login/obtain', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('login/refresh', TokenRefreshView.as_view(), name = 'token_refresh')

]