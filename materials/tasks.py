from celery import shared_task
from django.utils import timezone

# from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# from dogs.services import send_telegram_message
from users.models import User


@shared_task
def send_information_about_like(email):
    """Отправляет хозяину собаки письмо, когда собаке ставят лайк"""
    # message = 'Вашей собаке поставили лайк'
    # send_mail('Новый лайк!', message, EMAIL_HOST_USER, [email])
    # user = User.objects.get(email=email)
    # if user.tg_chat_id:
    #     # print(user.tg_chat_id, message)
    #     send_telegram_message(user.tg_chat_id, message)
    pass


@shared_task
def send_email_about_birthday():
    # today = timezone.now().date()
    # dogs = Dog.objects.filter(owner__isnull=False, date_born=today)
    # message = 'Поздравляем вашу собаку с Днём Рождения!'
    # email_list = []
    # for dog in dogs:
    #     email_list.append(dog.owner.email)
    #     if dog.owner.tg_chat_id:
    #         send_telegram_message(dog.owner.tg_chat_id, message)
    # if email_list:
    #     send_mail('Поздравление', message, EMAIL_HOST_USER, email_list)
    pass
