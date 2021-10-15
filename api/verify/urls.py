from django.urls import path

from api.verify.views import *

app_name = 'verify'
urlpatterns = [
    # 사용자 회원가입/프로필 업데이트 시 수행하는 중복 데이터 확인 URL
    path('nickname', NicknameVerifyView.as_view(), name='verify_nickname'),
    # 코치 등록 요청 시 수행하는 코치 코드의 유효성 검증 URL
    path('coachcode', CoachCodeVerifyView.as_view(), name='verify_coachcode'),
]
