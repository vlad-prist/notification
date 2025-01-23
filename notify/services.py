import requests
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status


def send_telegram_message(message_text, telegram_id):
    params = {"chat_id": telegram_id, "text": message_text}
    response = requests.post(
        f"{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
        params=params,
    )
    if response.status_code != status.HTTP_200_OK:
        raise Exception(f"Ошибка при отправке сообщения в Telegram: {response.text}")


def send_email_message(message_text, email):
    try:
        send_mail(
            subject='Новое уведомление',
            message=message_text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        print(f"Сообщение отправлено на {email}")
    except Exception as e:
        raise Exception(f"Ошибка при отправке сообщения на почту: {str(e)}")
