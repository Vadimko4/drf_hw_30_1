from celery import shared_task
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# from dogs.services import send_telegram_message
from users.models import User
from .models import Course, Subscription


@shared_task
def send_information_about_course_update(course_id):
    """Отправляет подписчикам письмо, когда курс обновляется"""
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)

        # Получаем список email подписанных пользователей
        subscriber_emails = subscriptions.values_list('user__email', flat=True)

        # Формируем и отправляем письмо каждому подписчику
        subject = f'Обновление курса "{course.title}"'
        message = f'Курс "{course.title}" был обновлен. Проверьте новые материалы!'

        for email in subscriber_emails:
            send_mail(
                subject=subject,
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

        return f"Уведомления отправлены {len(subscriber_emails)} подписчикам курса '{course.title}'"

    except Course.DoesNotExist:
        return "Курс не найден"
    except Exception as e:
        return f"Ошибка при отправке уведомлений: {str(e)}"


@shared_task
def block_inactive_users():
    today = timezone.now().date()
    users = User.objects.filter(is_active=True)
    for user in users:
        if user.last_login:
            last_login_date = user.last_login.date()
            time_delta = today - last_login_date
            if time_delta.days > 30:
                user.is_active = False
                user.save()
