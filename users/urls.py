from django.urls import path

from .views import *

app_name = 'users'
urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),

    path('profile/<int:pk>', UserProfileView.as_view(), name='main_profile'),
    path('profile/<int:pk>/edit', UserProfileView.as_view(), name='edit_main_profile'),
    path('profile/trainee/<int:pk>/sub', TraineeSubProfileView.as_view(), name='trainee_sub_profile'),
    path('profile/coach/<int:pk>/sub', CoachSubProfileView.as_view(), name='coach_sub_profile'),
    path('profile/coach/<int:pk>/evaluation', CoachEvaluationView.as_view(), name='coach_evaluation'),
]
