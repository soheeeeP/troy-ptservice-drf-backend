import json

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializer import ServiceDetailSerializer
from users.models import UserProfile, TraineeProfile, CoachProfile


# root에 저장할 Service 객체의 PK값 가져오기 (GET)
class ServiceView(generics.RetrieveAPIView):
    pass


# 함께하는 트레이너 정보 보여주기 (GET)
class ServiceCoachView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    queryset = TraineeProfile.objects.all()
    serializer_class = ServiceDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        trainee = self.get_object()
        response = {
            'coach': self.serializer_class.get_coach(obj=trainee)
        }
        return Response(response, status=status.HTTP_200_OK)


# 트레이너의 dashboard에서 활용할 view
class ServiceTraineeView(generics.GenericAPIView):
    pass


# 트레이니 운동 현황 (GET)
# T-Profile, T-Dashboard, C-Dashboard에서 모두 재사용될 component
class OnlineServiceView(generics.RetrieveAPIView):
    # OnlineService > list of Quest objs(mealplanner, workout, rate_feedback, quest_feedback)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    queryset = TraineeProfile.objects.all()
    serializer_class = ServiceDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        trainee = self.get_object()
        online = ServiceDetailSerializer.get_online_service(obj=trainee)

        quest_set = self.serializer_class.get_quest(obj=online)
        quest_total_score = self.serializer_class.get_total_score(obj=online, query=quest_set)

        # T-Profile에서는 'quest_total_score' 사용
        # T-Dashboard, C-Dashboard에서는 'quest_set' 사용
        feedback_list = quest_set.values_list('date', 'rate_feedback', 'quest_feedback')
        response = {
            'goal': self.serializer_class.get_goal(obj=trainee),
            'quest': quest_set,
            'score': quest_total_score,
            'feedback': feedback_list,
        }
        return Response(response, status=status.HTTP_200_OK)


class OfflineServiceView(generics.GenericAPIView):
    pass


# 트레이니의 운동 목표 설정 (GET), 수정 (PUT)
class TraineeGoalView(generics.RetrieveUpdateAPIView):
    pass


# 트레이니의 체중정보 입력 (GET)
class TraineeBodyInfoView(generics.RetrieveAPIView):
    pass
