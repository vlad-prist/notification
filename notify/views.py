from rest_framework import viewsets
from django.utils.timezone import localtime, now
from datetime import timedelta, datetime
from .serializers import RecipientSerializer, MessageSerializer
from .models import Recipient, Message
from .tasks import send_notify


class NotifyViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        delay_hours = {
            0: 0,  # Сразу
            1: 1,  # Через час
            2: 24  # Через день
        }
        delay = serializer.validated_data['delay']
        delay_delta = timedelta(hours=delay_hours[delay])

        scheduled_time = (localtime(now()) + delay_delta)
        message = serializer.save(scheduled_time=scheduled_time)

        send_notify.apply_async(
            args=[message.id],
            eta=scheduled_time
        )


class RecipientViewSet(viewsets.ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer

    def perform_create(self, serializer):
        recipient = serializer.save()
        recipient.save()
