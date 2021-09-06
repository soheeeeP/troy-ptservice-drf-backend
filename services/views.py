import json

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# root에 저장할 Service 객체의 PK값 가져오기 (GET)
class ServiceView(generics.RetrieveAPIView):
    pass


# 함께하는 트레이너 정보 보여주기 (GET)
class ServiceTrainerView(generics.RetrieveAPIView):
    pass


# 트레이너의 dashboard에서 활용할 view
class ServiceTraineeView(generics.GenericAPIView):
    pass


# 트레이니 운동 현황 (GET)
class OnlineServiceView(generics.RetrieveAPIView):
    # OnlineService > list of Quest objs(mealplanner, workout, rate_feedback, quest_feedback)
    # Service > coach_profile(name, center, specialty, profile_img)
    pass


class OfflineServiceView(generics.GenericAPIView):
    pass


# 트레이니의 운동 목표 설정 (GET), 수정 (PUT)
class TraineeGoalView(generics.RetrieveUpdateAPIView):
    pass


# 트레이니의 체중정보 입력 (GET)
class TraineeBodyInfoView(generics.RetrieveAPIView):
    pass
