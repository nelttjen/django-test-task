from rest_framework import serializers

from .models import Title, Tags, Volume, Chapter


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = ('id', 'chapter_number', 'chapter_content', 'chapter_views_count', 'chapter_likes_count')
        read_only_fields = ('chapter_number', 'chapter_content', 'chapter_views_count', 'chapter_likes_count')


class VolumeSerializer(serializers.ModelSerializer):
    volume_chapters = ChapterSerializer(many=True)

    class Meta:
        model = Volume
        fields = ('id', 'volume_name', 'volume_price', 'volume_number', 'volume_chapters')
        ordering = ('id', 'volume_name', 'volume_price', 'volume_number', 'volume_chapters')


class TitleSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)

    class Meta:
        model = Title
        fields = ('id', 'ru_name', 'en_name', 'alt_name', 'description', 'tags')
        ordering = ('id', 'ru_name', 'en_name', 'alt_name', 'description', 'tags')


class SingleTitleSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    volume_titles = VolumeSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'ru_name', 'en_name', 'alt_name', 'description', 'tags', 'volume_titles')
        ordering = ('id', 'ru_name', 'en_name', 'alt_name', 'description', 'tags', 'volume_titles')


class SingleChapterGetSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    data = ChapterSerializer()


class SingleChaprerGetErrorSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    data = serializers.JSONField(default={})


class ChapterPostLikeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    data = serializers.JSONField(read_only=True)

class ChapterResponseLikeSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)