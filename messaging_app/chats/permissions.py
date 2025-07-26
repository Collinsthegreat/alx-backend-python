# chats/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Allows only participants of a conversation to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - Only participants of the related conversation can access the message
        - Applies to GET, PUT, PATCH, DELETE
        """
        if request.method in ['PUT', 'PATCH', 'DELETE', 'GET']:
            conversation = getattr(obj, 'conversation', None)
            if not conversation:
                return False
            return request.user in conversation.participants.all()

        return True  # Allow other safe methods (e.g., HEAD, OPTIONS)


# chats/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS
from chats.models import Message

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow conversation participants to access or modify messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check that the user is a participant of the conversation
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        return False
