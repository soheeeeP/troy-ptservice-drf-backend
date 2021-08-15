from rest_framework import serializers

from .models import UserProfile, TraineeProfile, TrainerProfile


class AuthSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google', 'kakao', 'naver'])
    id_token = serializers.CharField()
    access_token = serializers.CharField()
    oauth = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()

    def validate(self, attrs):
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
