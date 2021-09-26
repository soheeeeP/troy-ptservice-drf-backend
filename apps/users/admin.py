from django.contrib import admin
from .models import UserProfile, TraineeProfile, CoachProfile

admin.site.register(UserProfile)
admin.site.register(TraineeProfile)
admin.site.register(CoachProfile)