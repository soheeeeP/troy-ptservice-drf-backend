from django.urls import path

from .views import *

app_name = 'users'
urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),

    path('profile/trainee/<int:pk>', TraineeProfileView.as_view(), name='trainee_profile'),
    path('profile/trainee/<int:pk>/edit', TrainerProfileView.as_view(), name='edit_trainee_profile'),
    path('profile/trainee/<int:pk>/sub', TraineeSubProfileView.as_view(), name='trainee_sub_profile'),

    path('profile/trainer/<int:pk>', TrainerProfileView.as_view(), name='trainer_profile'),
    path('profile/trainer/<int:pk>/edit', TrainerProfileView.as_view(), name='edit_trainer_profile'),
    path('profile/trainer/<int:pk>/sub', TrainerSubProfileView.as_view(), name='trainer_sub_profile'),
    path('profile/trainer/<int:pk>/evaluation', TrainerEvaluationView.as_view(), name='trainer_evaluation'),
]
