from django.urls import path

from api.programs.views import *

app_name = 'programs'
urlpatterns = [
    # 서비스 코치 list URL
    path('coach/all', CoachListView.as_view(), name='coach_all'),

    path('coach/evaluation', CoachEvaluationView.as_view(), name='coach_evaluation'),
    path('trainee/dashboard', ProgramView.as_view(), name='program'),
    path('trainee/coach_info', ProgramCoachView.as_view(), name='program_coach_info'),
]
