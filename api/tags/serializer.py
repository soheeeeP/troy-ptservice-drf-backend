from rest_framework import serializers

from apps.tags.models import HashTag


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ['tag_type', 'tag_content']

    def validate(self, attrs):
        return super(HashTagSerializer, self).validate(dict(attrs))


class HashTagCreateSerializer(serializers.Serializer):
    def create(self, validated_data):
        return super(HashTagCreateSerializer, self).create(validated_data)