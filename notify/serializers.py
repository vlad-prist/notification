from rest_framework import serializers
from .models import Recipient, Message


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'

    def validate(self, data):
        if not data.get('email') and not data.get('telegram'):
            raise serializers.ValidationError('Необходимо указать почту или телеграм-ник')
        return data

    def validate_recipients(self, value):
        for recipient in value:
            if not ("@" in recipient or recipient.isdigit()):
                raise serializers.ValidationError('Некорректные данные получателя')
        return value


class MessageSerializer(serializers.Serializer):
    message_text = serializers.CharField(max_length=1024)
    recipients = serializers.PrimaryKeyRelatedField(many=True, queryset=Recipient.objects.all())
    delay = serializers.IntegerField(min_value=0, max_value=2)
    scheduled_time = serializers.DateTimeField(
        required=False,
        format="%d.%m.%Y %H:%M"
    )

    class Meta:
        model = Message
        fields = ['message_text', 'recipients', 'delay', 'scheduled_time']

    def create(self, validated_data):
        recipients = validated_data.pop('recipients')
        message = Message.objects.create(**validated_data)
        message.recipients.set(recipients)
        return message
