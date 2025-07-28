
# Create your models here.
"""
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # Track edits

    def __str__(self):
        return f'From {self.sender} to {self.receiver}'

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'History for message {self.message.id}'
   """ 
from django.db import models
from django.contrib.auth.models import User

"""class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='chat_sent_messages'  # 👈 make this unique
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='chat_received_messages'  # 👈 make this unique
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {self.content[:30]}"
    """

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)  # ✅ New field
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # ✅ Custom manager

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'



class MessageHistory(models.Model):
   message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history_entries'
    )
old_content = models.TextField()
edited_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"


