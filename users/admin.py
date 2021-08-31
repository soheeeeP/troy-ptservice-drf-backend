from django.contrib import admin
from .models import UserProfile, TraineeProfile, TrainerProfile

admin.site.register(UserProfile)
admin.site.register(TraineeProfile)
admin.site.register(TrainerProfile)