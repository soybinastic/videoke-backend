from rest_framework import serializers

from rooms.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id", "session_id", "display_name", "is_host", "joined_at"]
        read_only_fields = ["id", "is_host", "joined_at"]
