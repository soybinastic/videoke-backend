from rooms.domain.constants import ALLOWED_REACTIONS, RoomEventType
from rooms.domain.exceptions import InvalidReactionError
from rooms.repositories import RoomRepository
from rooms.services.protocols import RoomEventBroadcaster


class ReactionService:
    """Handles live reactions and virtual applause."""

    def __init__(
        self,
        room_repository: RoomRepository,
        broadcaster: RoomEventBroadcaster,
    ) -> None:
        self._rooms = room_repository
        self._broadcaster = broadcaster

    def send_reaction(self, code: str, emoji: str, sender: str) -> None:
        if emoji not in ALLOWED_REACTIONS:
            raise InvalidReactionError()

        room = self._rooms.get_active_by_code(code)
        self._broadcaster.broadcast(
            room.code,
            RoomEventType.REACTION,
            {"emoji": emoji, "sender": sender},
        )

    def send_applause(self, code: str, sender: str) -> None:
        room = self._rooms.get_active_by_code(code)
        self._broadcaster.broadcast(
            room.code,
            RoomEventType.APPLAUSE,
            {"sender": sender},
        )
