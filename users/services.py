from decimal import Decimal

import requests
import stripe
from config.settings import STRIPE_API_KEY
# from forex_python.converter import CurrencyRates

stripe.api_key = STRIPE_API_KEY


# def convert_rub_to_dollars(amount):
#     """Конвертирует рубли в доллары"""
#     c = CurrencyRates()
#     rate = c.get_rate('RUB', 'USD')
#     return int(amount * rate)


def convert_rub_to_dollars(amount_rub):
    """
    Конвертирует рубли в доллары через внешний API
    """
    try:
        # Используем бесплатный API для курса валют
        response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB', timeout=5)
        data = response.json()
        rate = Decimal(str(data['rates']['USD']))
        amount_usd = amount_rub * rate
        return int(amount_usd)
    except Exception as e:
        # Запасной вариант
        print(f"Ошибка получения курса: {e}. Используется фиксированный курс.")
        fixed_rate = Decimal('0.011')
        amount_usd = amount_rub * fixed_rate
        return int(amount_usd)


def create_stripe_price(amount):
    """Создаёт цену в страйпе."""

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100, # если валюта будет рубли, то в копейках и тоже * 100
        # recurring={"interval": "month"}, это для регулярных платежей
        product_data={"name": "Education Payment"},
    )


def create_stripe_session(price):
    """Создаёт сессию на оплату в страйпе."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
