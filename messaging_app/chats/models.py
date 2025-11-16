import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# -----------------------------
# Custom User Model
# -----------------------------
class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds UUID user_id, phone_number, role, and timestamps.
    """
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")

    created_at = models.DateTimeField(auto_now_add=True)

    # Remove username uniqueness conflict (email becomes primary login field)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return f"{self.email}"


# -----------------------------
# Conversation Model
# -----------------------------
class Conversation(models.Model):
    """
    Stores a conversation between two or more users.
    Many-to-Many relationship with User as participants.
    """

    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )

    participants = models.ManyToManyField(User, related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# -----------------------------
# Message Model
# -----------------------------
class Message(models.Model):
    """
    Stores a message belonging to a conversation.
    Each message has one sender and belongs to one conversation.
    """

    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )

    message_body = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} in {self.conversation.conversation_id}"
