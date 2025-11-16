from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import User, Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    UserSerializer,
)


# ----------------------------------------------------
# Conversation ViewSet
# ----------------------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, retrieving conversations.
    Allows creating a conversation and adding participants.
    """

    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with multiple participants.
        Expected payload:
        {
            "participants": ["uuid1", "uuid2"]
        }
        """
        participant_ids = request.data.get("participants", [])

        if not participant_ids:
            return Response(
                {"error": "Participants list is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch users
        users = User.objects.filter(user_id__in=participant_ids)

        if len(users) != len(participant_ids):
            return Response(
                {"error": "One or more participant IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        conversation.save()

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def add_participant(self, request, pk=None):
        """
        Add a participant to an existing conversation.
        """
        conversation = self.get_object()
        user_id = request.data.get("user_id")

        if not user_id:
            return Response(
                {"error": "user_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, user_id=user_id)
        conversation.participants.add(user)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ----------------------------------------------------
# Message ViewSet
# ----------------------------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating messages.
    To send a message, user provides sender_id, message_body,
    and conversation_id.
    """

    queryset = Message.objects.all().order_by("-sent_at")
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expected payload:
        {
            "sender_id": "uuid",
            "conversation_id": "uuid",
            "message_body": "Hello!"
        }
        """
        sender_id = request.data.get("sender_id")
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        if not sender_id or not conversation_id or not message_body:
            return Response(
                {"error": "sender_id, conversation_id, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sender = get_object_or_404(User, user_id=sender_id)
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        # Validate sender belongs to conversation
        if sender not in conversation.participants.all():
            return Response(
                {"error": "Sender is not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Create message
        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body,
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
