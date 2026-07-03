"""Domain constants."""

ALLOWED_REACTIONS = frozenset({"👏", "😂", "❤️"})


class RoomEventType:
    QUEUE_UPDATED = "queue_updated"
    SONG_SKIPPED = "song_skipped"
    REACTION = "reaction"
    APPLAUSE = "applause"
    PARTICIPANT_JOINED = "participant_joined"
    HOST_CHANGED = "host_changed"
    VOICE_SIGNAL = "voice_signal"
