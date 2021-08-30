from rest_framework import serializers

from .models import HashTag

class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ['tag_type', 'tag_content']

    def create(self, validated_data):
        return super(HashTagSerializer, self).create(validated_data)

