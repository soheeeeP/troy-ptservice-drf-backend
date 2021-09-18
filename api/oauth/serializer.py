from rest_framework import serializers

from apps.oauth.models import Auth


class AuthDefaultSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google', 'kakao', 'naver'])
    id_token = serializers.CharField()
    access_token = serializers.CharField()
    oauth = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()

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
