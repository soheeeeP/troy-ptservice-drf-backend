from rest_framework import serializers

from apps.centers.models import Center


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = '__all__'
    
    def validate(self, attrs):
        return attrs