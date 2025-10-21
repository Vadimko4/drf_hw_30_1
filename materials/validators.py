import re

from rest_framework.serializers import ValidationError


# def has_external_links(text):
#     """
#     Быстрая проверка на наличие внешних ссылок (кроме YouTube)
#     """
#     youtube_pattern = re.compile(
#         r'(https?://)?(www\.)?(youtube\.com|youtu\.be)',
#         re.IGNORECASE
#     )
#
#     # Убираем YouTube ссылки из текста
#     text_without_youtube = youtube_pattern.sub('', text)
#
#     # Проверяем оставшийся текст на наличие других URL
#     url_pattern = re.compile(
#         r'(https?://|ftp://)?'  # протокол
#         r'([a-z0-9-]+\.)+[a-z]{2,63}'  # домен
#         r'|'
#         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'  # IPv4
#         r'|'
#         r'[a-z0-9-]+\.[a-z]{2,63}'  # домен без протокола
#         , re.IGNORECASE)
#
#     return bool(url_pattern.search(text_without_youtube))


# Быстрое тестирование
# test_texts = [
#     "youtube.com - разрешено",
#     "google.com - запрещено",
#     "youtu.be/abc - разрешено",
#     "site.ru - запрещено"
# ]
#
# for text in test_texts:
#     has_external = has_external_links(text)
#     print(f"'{text}' -> Внешние ссылки: {has_external}")

def has_external_links(text):
    """
    Более точная проверка на внешние ссылки
    """
    if not text or not isinstance(text, str):
        return False

    # Ищем только полноценные URL с протоколом
    url_pattern = re.compile(
        r'https?://(?!.*(youtube|youtu\.be))[^\s]+',
        re.IGNORECASE
    )

    return bool(url_pattern.search(text))


def validate_external_links(value):
    if has_external_links(value):
        raise ValidationError("Использована ссылка на внешний ресурс - это запрещено")
