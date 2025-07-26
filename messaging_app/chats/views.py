# messaging_app/chats/views.py

"""Viewsets for Conversation and Message models"""

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import (
    ConversationDetailSerializer,
    ConversationListSerializer,
    MessageSerializer,
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations
    """

    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]  # Disable PUT/PATCH/DELETE
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    search_fields = [
        "participants__first_name",
        "participants__last_name",
        "participants__email",
    ]

    def get_queryset(self):
        # Get conversations where current user is a participant
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related("participants", "messages")

    def get_serializer_class(self):
        if self.action == "list":
            return ConversationListSerializer
        return ConversationDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Add current user to participants if not included
        participants = serializer.validated_data.get("participants", [])
        if request.user not in participants:
            participants.append(request.user)

        conversation = serializer.save(participants=participants)
        return Response(
            ConversationDetailSerializer(conversation).data,
            status=status.HTTP_201_CREATED,
        )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages within a conversation
    """

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]  # Disable PUT/PATCH/DELETE
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["sender__role"]
    ordering_fields = ["sent_at"]
    ordering = ["-sent_at"]
    search_fields = ["message_body", "sender__first_name", "sender__last_name"]

    def get_queryset(self) -> "QuerySet[Message]":
        # Get conversation ID from URL
        conversation_id = self.kwargs.get("conversation_id")

        # Verify conversation exists and user is participant
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation")

        # Return messages for this conversation with optimized queries
        return (
            Message.objects.filter(conversation=conversation)
            .select_related("sender", "conversation")
            .order_by("-sent_at")
        )

    def create(self, request, *args, **kwargs):
        # Get conversation ID from URL
        conversation_id = self.kwargs.get("conversation_id")

        # Verify conversation exists and user is participant
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found")

        if request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation")

        # Create message with current user as sender
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(sender=request.user, conversation=conversation)

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

#
# chats/views.py

# chats/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chats.models import Message
from chats.serializers import MessageSerializer
from chats.permissions import IsParticipantOfConversation
from rest_framework.status import HTTP_403_FORBIDDEN  # ✅ EXPLICIT IMPORT

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
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user)

# chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN
from django_filters.rest_framework import DjangoFilterBackend

from chats.models import Message
from chats.serializers import MessageSerializer
from chats.permissions import IsParticipantOfConversation
from chats.filters import MessageFilter
from chats.pagination import StandardResultsSetPagination

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for messages. Paginates and filters results, restricts access to participants.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user)


