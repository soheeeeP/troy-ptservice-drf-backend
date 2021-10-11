from rest_framework import serializers

from apps.tags.models import HashTag


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ['tag_type', 'tag_content']

    def validate(self, attrs):
        return super(HashTagSerializer, self).validate(dict(attrs))


class HashTagCreateSerializer(serializers.Serializer):
    @staticmethod
    def bulk_create_tags_list(tags):
        if tags is None:
            return
        tags_list = [HashTag(tag_type=x['tag_type'], tag_content=x['tag_content']) for x in tags]
        tags_obj = HashTag.objects.bulk_create(tags_list)
        for t in tags_obj:
            t.save()
        return tags_obj

    def create(self, validated_data):
        return super(HashTagCreateSerializer, self).create(validated_data)