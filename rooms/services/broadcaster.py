from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rooms.services.protocols import RoomEventBroadcaster


class ChannelsRoomEventBroadcaster:
    """Concrete broadcaster using Django Channels."""

    def broadcast(self, room_code: str, event_type: str, data: dict) -> None:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"room_{room_code}",
            {"type": "room.event", "event": event_type, "data": data},
        )
