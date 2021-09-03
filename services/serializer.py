from rest_framework import serializers

from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        
    def validate(self, attrs):
        return dict(attrs)
    
    def create(self, validated_data):
        return super(GoalSerializer, self).create(validated_data)
