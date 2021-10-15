from django.core.cache import caches

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ScheduleRequestView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    pass


class RescheduleRequestView(generics.CreateAPIView):
    pass


class RescheduleResponseView(generics.CreateAPIView):
    pass
