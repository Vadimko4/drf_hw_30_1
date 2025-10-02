from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import SET_NULL
from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")
    phone = models.CharField(max_length=35, verbose_name="Телефон", blank=True, null=True,
                             help_text="Введите номер телефона")
    town = models.CharField(max_length=50, verbose_name="Город", blank=True, null=True,
                               help_text="Введите город")
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True,
                               help_text="Загрузите свой аватар")

    USERNAME_FIELD = "email" # меняем юзернейм на почту
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_TYPE = [
        ('cash', 'Наличные'),
        ('transaction', 'Перевод'),
    ]

    user = models.ForeignKey(User, verbose_name='Плательщик', help_text='Укажите плательщика',
                             on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс',
                        help_text='Укажите курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок',
                        help_text='Укажите оплаченный урок')
    date = models.DateField(verbose_name='Дата оплаты', help_text='Введите дату оплаты')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты', help_text='Введите сумму оплаты')
    type = models.CharField(max_length=12, choices=PAYMENT_TYPE)

    def __str__(self):
        return f'{self.user}: {self.amount}, {self.type}'

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
