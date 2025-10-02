from django.contrib import admin
from materials.models import Course, Lesson


@admin.register(Lesson)  # Регистрируем модель
class LessonAdmin(admin.ModelAdmin):
    # Настраиваем поля, которые будем выводить в админке
    list_display = ('id', 'title', 'course')
    # По чему будем делать фильтрацию
    list_filter = ('id', 'course')
    # По чему у нас будет поиск
    search_fields = ('title', 'course')


@admin.register(Course)  # Регистрируем модель
class CourseAdmin(admin.ModelAdmin):
    # Настраиваем поля, которые будем выводить в админке
    list_display = ('id', 'title',)
