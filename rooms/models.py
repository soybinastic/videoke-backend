import secrets
import string
import uuid

from django.db import models


def generate_room_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(6))


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=6, unique=True, default=generate_room_code)
    name = models.CharField(max_length=100)
    host_session_id = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

    def is_host(self, session_id: str) -> bool:
        return self.host_session_id == session_id

    def get_now_playing(self) -> "QueueItem | None":
        return self.queue_items.filter(status=QueueItem.Status.PLAYING).first()


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="participants")
    session_id = models.CharField(max_length=64)
    display_name = models.CharField(max_length=50)
    is_host = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["room", "session_id"]
        ordering = ["joined_at"]

    def __str__(self) -> str:
        return self.display_name


class QueueItem(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        PLAYING = "playing", "Playing"
        DONE = "done", "Done"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="queue_items")
    youtube_url = models.URLField(max_length=500)
    video_id = models.CharField(max_length=20)
    title = models.CharField(max_length=200, blank=True)
    added_by_name = models.CharField(max_length=50)
    position = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.QUEUED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "created_at"]

    def __str__(self) -> str:
        return self.title or self.video_id

    def mark_playing(self) -> None:
        self.status = self.Status.PLAYING
        self.save(update_fields=["status"])

    def mark_done(self) -> None:
        self.status = self.Status.DONE
        self.save(update_fields=["status"])
