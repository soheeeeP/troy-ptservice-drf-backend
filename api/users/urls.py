from django.urls import path

from api.users.views import *

app_name = 'users'
urlpatterns = [
    # 사용자 회원가입/로그인 URL
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),

    # 사용자 프로필 조회 URL
    path('profile/main', UserProfileView.as_view(), name='mainprofile'),
    path('profile/trainee/sub', TraineeSubProfileView.as_view(), name='trainee_subprofile'),
    path('profile/coach/sub', CoachSubProfileView.as_view(), name='coach_subprofile'),

    # 사용자 프로필 업데이트 URL
    path('profile/edit', ProfileUpdateView.as_view(), name='edit_profile'),

    # 서비스 코치 list URL
    path('coach/all', CoachListView.as_view(), name='coach_all'),
]
