from django.urls import path

from .views import AuthView

app_name = 'oauth'
urlpatterns = [
    path('validate', AuthView.as_view(), name='validate'),
]
