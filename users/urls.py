from django.urls import path

from .views import LoginView, SignUpView

app_name = 'users'
urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
]
