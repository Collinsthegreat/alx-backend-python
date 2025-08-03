from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user: User):
        """
        Returns unread messages where the given user is the receiver.
        """
        return self.filter(receiver=user, read=False)
