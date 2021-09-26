from rest_framework import serializers

from apps.oauth.models import Auth


class AuthDefaultSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google', 'kakao', 'naver'], help_text='oauth provider')
    id_token = serializers.CharField(help_text='oauth token')
    oauth_token = serializers.CharField(help_text='oauth id')

    def validate(self, attrs):
        return attrs


class AuthCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        auth, created = self.Meta.model.objects.get_or_create(**validated_data)
        if not created:
            raise serializers.ValidationError('oauth_value user already exists')
        return auth
