from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentDetailSerializer(ModelSerializer):
    # lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    # lesson_count = SerializerMethodField()
    #
    #
    # def get_lesson_count(self, course):
    #     return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
