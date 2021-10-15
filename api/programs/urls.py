from django.urls import path

from api.programs.views import *

app_name = 'programs'
urlpatterns = [
    # 코치, 트레이너 프로필의 component URL
    path('coach/evaluation', CoachEvaluationView.as_view(), name='coach_evaluation'),
    path('trainee/dashboard', ProgramView.as_view(), name='program'),
    path('trainee/coach_info', ProgramCoachView.as_view(), name='program_coach_info'),

    # 새로운 코치 등록 요청/응답 URL
    path('request', ProgramRequestView.as_view(), name='program_request'),
    path('response', ProgramResponseView.as_view(), name='program_response'),
]
