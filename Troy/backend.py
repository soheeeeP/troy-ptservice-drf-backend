from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class PasswordlessBackend(ModelBackend):
    def __init__(self):
        self.user = get_user_model()

    def authenticate(self, request, email=None, **kwargs):
        try:
            user = get_user_model().objects.get(email=email)
            return user
        except get_user_model().user.DoesNotExist:
            return None

    def get_user(self, user_pk):
        try:
            return get_user_model().objects.get(pk=user_pk)
        except get_user_model().DoesNotExist:
            return None
