from rest_framework import serializers

from rooms.models import QueueItem
from rooms.parsers import get_video_url_parser


class QueueItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueItem
        fields = [
            "id",
            "youtube_url",
            "video_id",
            "title",
            "added_by_name",
            "position",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "video_id", "position", "status", "created_at"]


class AddQueueItemSerializer(serializers.Serializer):
    youtube_url = serializers.URLField(max_length=500)
    added_by_name = serializers.CharField(max_length=50)
    session_id = serializers.CharField(max_length=64)
    title = serializers.CharField(max_length=200, required=False, allow_blank=True, default="")

    def validate_youtube_url(self, value: str) -> str:
        if not get_video_url_parser().extract_video_id(value):
            raise serializers.ValidationError("Invalid YouTube URL.")
        return value
