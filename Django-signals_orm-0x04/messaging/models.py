
# Create your models here.
"""from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='msg_sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='msg_received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:30]}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID: {self.message.id}"
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # ✅ Optional: Useful for manual timestamps
from .managers import UnreadMessagesManager  # ✅ Add this import at the top


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='msg_sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='msg_received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ✅ Tracks if the message has been read
    read = models.BooleanField(default=False)

    # ✅ Added to track if the message was edited
    edited = models.BooleanField(default=False)

    # ✅ Added to store when the message was last edited
    edited_at = models.DateTimeField(null=True, blank=True)

    # ✅ Added to store who edited the message
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')

    # ✅ Custom manager for unread messages
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:30]}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID: {self.message.id}"


# ✅ Added to keep history of old message content when edited
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message ID {self.message.id} at {self.edited_at}"
