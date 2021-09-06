from django.urls import path

from .views import *

app_name = 'services'
urlpatterns = [
    path('',ServiceView.as_view(), name='service'),
    path('<int:pk>/trainer_info', ServiceTrainerView.as_view(), name='service_trainer_info'),
    path('<int:pk>/online', OnlineServiceView.as_view(), name='online_service'),
    path('<int:pk>/trainee/goal/create',TraineeGoalView.as_view(), name='trainee_new_goal'),
    path('<int:pk>/trainee/goal/edit',TraineeGoalView.as_view(), name='edit_trainee_goal'),
    path('<int:pk>/trainee/body_info/create',TraineeBodyInfoView.as_view(), name='trainee_new_bodyinfo'),
]
