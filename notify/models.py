from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    objects = models.Manager()
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="время создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="время последнего изменения"
    )

    class Meta:
        abstract = True


class Recipient(BaseModel):
    """ Хранит информацию о получателе. """
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, null=True, blank=True)
    telegram = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="tg nickname"
    )

    def clean(self):
        if not self.email and not self.telegram:
            raise ValidationError('Необходимо указать почту или телеграм-ник')

    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.email or self.telegram})'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class Message(BaseModel):
    """ Хранит информацию о сообщении и получателях. """
    message_text = models.TextField(max_length=1024)
    recipients = models.ManyToManyField(Recipient, related_name='messages')
    delay = models.IntegerField()
    scheduled_time = models.DateTimeField()

    def __str__(self):
        return f'{self.message_text[:20]}...'

    class Meta:
        ordering = ('-scheduled_time',)
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


class MessageLog(BaseModel):
    """ Логирует все попытки отправки. """
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    sent_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(null=True, blank=True)
