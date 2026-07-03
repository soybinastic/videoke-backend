from rest_framework import serializers

from rooms.models import Room

from .participant_serializers import ParticipantSerializer
from .queue_serializers import QueueItemSerializer


class RoomSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    queue_items = QueueItemSerializer(many=True, read_only=True)
    now_playing = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "id",
            "code",
            "name",
            "host_session_id",
            "is_active",
            "created_at",
            "participants",
            "queue_items",
            "now_playing",
        ]
        read_only_fields = ["id", "code", "host_session_id", "created_at"]

    def get_now_playing(self, obj: Room) -> dict | None:
        item = obj.get_now_playing()
        if item:
            return QueueItemSerializer(item).data
        return None


class CreateRoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    host_name = serializers.CharField(max_length=50)
    session_id = serializers.CharField(max_length=64)


class JoinRoomSerializer(serializers.Serializer):
    display_name = serializers.CharField(max_length=50)
    session_id = serializers.CharField(max_length=64)


class TransferHostSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=64)
    participant_id = serializers.UUIDField()
