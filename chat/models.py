# chat/models.py

from django.db import models

from register.models import User


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} to {self.recipient.username}: {self.id}'