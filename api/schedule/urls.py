from django.urls import path

from api.schedule.views import *

app_name = 'schedule'
urlpatterns = [
    # 주간 스케줄 등록 URL
    path('coach/weekly/new', ),
    path('coach/weekly/edit',),

    # 스케줄 등록 및 취소에 대한 요청 URL
    path('trainee/request/schedule/new', ScheduleRequestView.as_view(), name='new_schedule_request'),
    path('trainee/request/schedule/cancel', ScheduleRequestView.as_view(), name='cancel_schedule_request'),

    # 스케줄 변경에 대한 요청/응답 URL
    path('trainee/request/reschedule', RescheduleRequestView.as_view(), name='reschedule_request'),
    path('coach/response/reschedule', RescheduleResponseView.as_view(), name='reschedule_response'),
]
