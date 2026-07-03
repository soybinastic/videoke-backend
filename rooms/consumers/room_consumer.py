import json

from channels.generic.websocket import AsyncWebsocketConsumer

from rooms.consumers.handlers import WebSocketMessageDispatcher


class RoomConsumer(AsyncWebsocketConsumer):
    """WebSocket endpoint for real-time room events."""

    _dispatcher = WebSocketMessageDispatcher()

    async def connect(self) -> None:
        self.room_code = self.scope["url_route"]["kwargs"]["code"].upper()
        self.room_group_name = f"room_{self.room_code}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data: str | None = None, bytes_data: bytes | None = None) -> None:
        if not text_data:
            return
        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message_type = payload.get("type")
        if message_type:
            await self._dispatcher.dispatch(self, message_type, payload)

    async def room_event(self, event: dict) -> None:
        await self.send(
            text_data=json.dumps(
                {
                    "type": event["event"],
                    "data": event["data"],
                }
            )
        )
