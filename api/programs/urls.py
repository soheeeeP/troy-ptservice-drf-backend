from django.urls import path

from .views import *

app_name = 'programs'
urlpatterns = [
    path('<int:pk>/coach/evaluation', CoachEvaluationView.as_view(), name='coach_evaluation'),
    path('<int:pk>/trainee/dashboard', ProgramView.as_view(), name='program'),
    path('<int:pk>/trainee/coach_info', ProgramCoachView.as_view(), name='program_coach_info'),
    path('<int:pk>/trainee/goal/create',TraineeGoalView.as_view(), name='trainee_new_goal'),
    path('<int:pk>/trainee/goal/edit',TraineeGoalView.as_view(), name='edit_trainee_goal'),
    path('<int:pk>/trainee/body_info/create',TraineeBodyInfoView.as_view(), name='trainee_new_bodyinfo'),
]
