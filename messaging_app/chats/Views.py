from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from chats.models import Message
from chats.serializers import MessageSerializer
from chats.permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage messages within a conversation.
    Access restricted to participants only.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Filter messages to only those in conversations where the user is a participant.
        This prevents unauthorized access even before hitting has_object_permission.
        """
        return Message.objects.filter(conversation__participants=self.request.user)

