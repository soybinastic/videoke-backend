from abc import ABC, abstractmethod


class WebSocketMessageHandler(ABC):
    """Strategy interface for handling inbound WebSocket messages."""

    @abstractmethod
    async def handle(self, consumer, payload: dict) -> None:
        """Process a parsed WebSocket payload."""


class VoiceSignalHandler(WebSocketMessageHandler):
    """Relays WebRTC voice signaling to all room participants."""

    async def handle(self, consumer, payload: dict) -> None:
        from rooms.domain.constants import RoomEventType

        await consumer.channel_layer.group_send(
            consumer.room_group_name,
            {
                "type": "room.event",
                "event": RoomEventType.VOICE_SIGNAL,
                "data": {
                    "sender": payload.get("sender"),
                    "signal": payload.get("signal"),
                    "target": payload.get("target"),
                },
            },
        )


class WebSocketMessageDispatcher:
    """Routes inbound messages to the appropriate handler (Strategy + Registry)."""

    def __init__(self) -> None:
        self._handlers: dict[str, WebSocketMessageHandler] = {
            "voice_signal": VoiceSignalHandler(),
        }

    async def dispatch(self, consumer, message_type: str, payload: dict) -> None:
        handler = self._handlers.get(message_type)
        if handler:
            await handler.handle(consumer, payload)
