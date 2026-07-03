from uuid import UUID

from rooms.domain.constants import RoomEventType
from rooms.domain.exceptions import DomainError
from rooms.domain.host_guard import assert_is_host
from rooms.models import Room
from rooms.repositories import ParticipantRepository, RoomRepository
from rooms.serializers import RoomSerializer
from rooms.services.protocols import RoomEventBroadcaster


class RoomService:
    """Orchestrates room lifecycle: create, join, host transfer, and state retrieval."""

    def __init__(
        self,
        room_repository: RoomRepository,
        participant_repository: ParticipantRepository,
        broadcaster: RoomEventBroadcaster,
    ) -> None:
        self._rooms = room_repository
        self._participants = participant_repository
        self._broadcaster = broadcaster

    def create_room(self, name: str, host_name: str, session_id: str) -> dict:
        room = self._rooms.create(name=name, host_session_id=session_id)
        self._participants.create_host(room, session_id, host_name)
        return self.serialize_room(room)

    def get_room(self, code: str) -> dict:
        room = self._rooms.get_active_by_code(code)
        return self.serialize_room(room)

    def join_room(self, code: str, display_name: str, session_id: str) -> dict:
        room = self._rooms.get_active_by_code(code)
        participant, created = self._participants.get_or_create(room, session_id, display_name)
        state = self.serialize_room(room)

        if created:
            self._broadcaster.broadcast(room.code, RoomEventType.PARTICIPANT_JOINED, state)

        return state

    def transfer_host(self, code: str, session_id: str, participant_id: UUID) -> dict:
        room = self._rooms.get_active_by_code(code)
        assert_is_host(room, session_id, "transfer host privileges")

        target = self._participants.get_by_id(room, str(participant_id))
        if target.session_id == session_id:
            raise DomainError("You are already the host.")

        self._participants.clear_host_flags(room)
        self._participants.promote_to_host(target)
        self._rooms.update_host(room, target.session_id)

        state = self.serialize_room(room)
        self._broadcaster.broadcast(room.code, RoomEventType.HOST_CHANGED, state)
        return state

    def serialize_room(self, room: Room) -> dict:
        return RoomSerializer(room).data
