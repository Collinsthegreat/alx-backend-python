# chats/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chats.models import Message
from chats.serializers import MessageSerializer
from chats.permissions import IsParticipantOfConversation
from rest_framework.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages. Only conversation participants can access.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Return only messages from conversations the user is participating in.
        """
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """
        Allow message creation only if the user is a participant of the conversation.
        """
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant of this conversation.")
        serializer.save(sender=self.request.user)


from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

@cache_page(60)
@login_required
def conversation_view(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'chats/conversation.html', {'messages': messages})
