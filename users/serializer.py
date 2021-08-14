from rest_framework import serializers

from .models import UserProfile, TraineeProfile, TrainerProfile


class AuthSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google', 'kakao', 'naver'])
    id_token = serializers.CharField()
    email = serializers.EmailField()
    access_token = serializers.CharField()

    def validate(self, attrs):
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'