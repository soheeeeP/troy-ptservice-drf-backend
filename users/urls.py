from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import LoginView, SignUpView

app_name = 'users'
urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),

    path('token/obtain',TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh', TokenRefreshView.as_view(), name = 'token_refresh')

]
