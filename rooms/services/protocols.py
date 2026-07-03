from typing import Protocol


class RoomEventBroadcaster(Protocol):
    """Observer interface for broadcasting real-time room events (DIP)."""

    def broadcast(self, room_code: str, event_type: str, data: dict) -> None: ...
