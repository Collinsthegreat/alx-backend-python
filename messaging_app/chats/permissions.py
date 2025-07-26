from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow access only to authenticated users
    who are participants of the conversation.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant of the conversation related to the message.
        `obj` is expected to be a Message instance with a `.conversation` attribute.
        """
        conversation = getattr(obj, 'conversation', None)
        if conversation is None:
            return False

        # Assuming conversation has a ManyToManyField or a related manager for participants
        return request.user in conversation.participants.all()
