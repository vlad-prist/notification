from celery import shared_task
from django.utils.timezone import now
from notify.models import Message, MessageLog
from notify.services import send_telegram_message, send_email_message


@shared_task
def send_notify(*args):
    current_time = now()
    messages = Message.objects.filter(
        scheduled_time__lte=current_time
    )
    for message in messages:
        for recipient in message.recipients.all():
            try:
                if recipient.email:
                    send_email_message(message.message_text, recipient.email)
                elif recipient.telegram:
                    send_telegram_message(message.message_text, recipient.telegram)
                MessageLog.objects.create(
                    message=message,
                    recipient=recipient,
                    status='SUCCESS'
                )
            except Exception as e:
                MessageLog.objects.create(
                    message=message,
                    recipient=recipient,
                    status='ERROR',
                    error_message=str(e)
                )
