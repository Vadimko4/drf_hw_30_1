from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', help_text='Введите название курса')
    preview = models.ImageField(upload_to="materials/courses_preview/", verbose_name="Превью", blank=True, null=True,
                               help_text="Загрузите превью курса")
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса',
                                   help_text='Введите описание курса')
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец",
                              help_text="Укажите владельца")
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Stripe Product ID',
        help_text='ID продукта в Stripe'
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', help_text='Введите название урока')
    description = models.TextField(blank=True, null=True, verbose_name='Описание урока',
                                   help_text='Введите описание урока')
    preview = models.ImageField(upload_to="materials/lessons_preview/", verbose_name="Превью", blank=True, null=True,
                                help_text="Загрузите превью урока")
    video_link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка на видео урока',
                                   help_text='Введите ссылку на видео урока')
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, verbose_name='Курс',
                        help_text='Введите курс', blank=True, null=True)
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец",
                              help_text="Укажите владельца")
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Stripe Product ID',
        help_text='ID продукта в Stripe'
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name="Курс")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ('user', 'course')  # Запрещает повторные подписки

    def __str__(self):
        return f"{self.user} - {self.course}"
