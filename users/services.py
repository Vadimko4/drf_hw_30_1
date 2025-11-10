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


# def create_stripe_price(amount):
#     """Создаёт цену в страйпе."""
#
#     return stripe.Price.create(
#         currency="usd",
#         unit_amount=amount * 100, # если валюта будет рубли, то в копейках и тоже * 100
#         # recurring={"interval": "month"}, это для регулярных платежей
#         product_data={"name": "Education Payment"},
#     )


# def create_stripe_session(price):
#     """Создаёт сессию на оплату в страйпе."""
#     session = stripe.checkout.Session.create(
#         success_url="http://127.0.0.1:8000/",
#         line_items=[{"price": price.get('id'), "quantity": 1}],
#         mode="payment",
#     )
#     return session.get('id'), session.get('url')


def create_stripe_product_and_price(payment):
    """
    Создает продукт и цену в Stripe на основе данных платежа
    """
    try:
        # Определяем название продукта на основе курса или урока
        if payment.course:
            product_name = f"Курс: {payment.course.title}"
            product_description = payment.course.description or f"Оплата курса {payment.course.title}"
        elif payment.lesson:
            product_name = f"Урок: {payment.lesson.title}"
            product_description = payment.lesson.description or f"Оплата урока {payment.lesson.title}"
        else:
            product_name = "Образовательный материал"
            product_description = "Оплата образовательного материала"

        # 1. Создаем продукт в Stripe
        product = stripe.Product.create(
            name=product_name,
            description=product_description,
        )

        # 2. Создаем цену, привязанную к продукту
        price = stripe.Price.create(
            product=product.id,  # Связываем цену с продуктом
            unit_amount=payment.amount * 100,  # Умножаем на 100 для копеек
            currency="rub",
        )

        # 3. Создаем сессию оплаты
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.id,  # Используем ID цены
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:8000/payments/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8000/payments/cancel',
        )

        return session.id, session.url

    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None, None
