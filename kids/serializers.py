from rest_framework import serializers
from .models import Course, Lesson, LessonVideo, LessonPoster


class LessonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideo
        fields = ['title', 'video_url', 'order']

class LessonPosterSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = LessonPoster
        fields = ['title', 'image_url', 'description']
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

class LessonSerializer(serializers.ModelSerializer):
    videos = LessonVideoSerializer(many=True, read_only=True)
    posters = LessonPosterSerializer(many=True, read_only=True)
    poster_image = serializers.SerializerMethodField()
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'lesson_type', 'order', 'poster_image', 'videos', 'posters', 'video_url']
    def get_poster_image(self, obj):
        return obj.poster_image.url if obj.poster_image else None

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = '__all__'
