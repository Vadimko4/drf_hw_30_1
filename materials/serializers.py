from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from materials.models import Course, Lesson
from materials.validators import validate_external_links


# Базовый сериализатор урока (полная версия)
class LessonSerializer(ModelSerializer):
    title = serializers.CharField(validators=[validate_external_links])
    description = serializers.CharField(validators=[validate_external_links])

    class Meta:
        model = Lesson
        fields = "__all__"


# Упрощенный сериализатор для интеграции в курс
class LessonInCourseSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title", "preview", "description", "video_link")
        # Исключаем поле 'course', так как оно избыточно при отображении внутри курса


class CourseSerializer(ModelSerializer):
    title = serializers.CharField(validators=[validate_external_links])
    description = serializers.CharField(validators=[validate_external_links])

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonInCourseSerializer(many=True, read_only=True, source='lesson_set')
    lesson_count = SerializerMethodField()


    def get_lesson_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("title", "preview", "description", "lesson_count", "lessons")
