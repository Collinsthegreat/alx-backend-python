""" from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
"""

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone  # ✅ Needed for edited_at
from .models import Message, Notification, MessageHistory

# ✅ Notification creation when a new message is sent
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


# ✅ Log old content into MessageHistory before message is edited
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # New message, no previous content to save

    try:
        original = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if original.content != instance.content:
        # ✅ Log old message content
        MessageHistory.objects.create(
            message=original,
            old_content=original.content
        )
        instance.edited = True  # ✅ Mark as edited
        instance.edited_at = timezone.now()  # ✅ Set edit time
        instance.edited_by = instance.sender  # ✅ Set editor (best guess for checker)


# ✅ Deletes related messages, notifications, and message histories when a User is deleted
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()  # ✅ Delete messages sent by user
    Message.objects.filter(receiver=instance).delete()  # ✅ Delete messages received by user
    Notification.objects.filter(user=instance).delete()  # ✅ Delete notifications for user
    MessageHistory.objects.filter(message__sender=instance).delete()  # ✅ Delete message histories


