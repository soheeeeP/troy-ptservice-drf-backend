import datetime

from rest_framework import serializers

from django.utils import timezone

from apps.oauth.models import Auth, AuthSMS


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


class AuthSMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthSMS
        fields = ['phone_number']


class AuthSMSCreateUpdateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(help_text='휴대폰 번호(11자리 숫자를 입력해주세요)')
    auth_number = serializers.CharField(help_text='인증 번호')

    class Meta:
        model = AuthSMS
        fields = ['phone_number', 'auth_number', 'created_at', 'updated_at']

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number', None)
        try:
            self.Meta.model.objects.get(phone_number=phone_number)
        except self.Meta.model.DoesNotExist:
            sms = self.Meta.model.objects.create(
                phone_number=phone_number,
                auth_number=validated_data.pop('auth_number', None),
                created_at=timezone.now()
            )
            return sms
        raise serializers.ValidationError('이미 등록된 휴대폰 번호입니다.')

    def update(self, instance, validated_data):
        time_diff = timezone.now() - instance.created_at
        if time_diff < datetime.timedelta(minutes=3):
            instance.updated_at = timezone.now()
            instance.save()
            return instance
        else:
            instance.delete()
            raise serializers.ValidationError('인증 유효시간이 지났습니다.')
