from django.shortcuts import get_object_or_404

from rooms.models import Participant, QueueItem, Room


class RoomRepository:
    """Data access for Room entities."""

    def get_active_by_code(self, code: str) -> Room:
        return get_object_or_404(Room, code=code.upper(), is_active=True)

    def create(self, name: str, host_session_id: str) -> Room:
        return Room.objects.create(name=name, host_session_id=host_session_id)

    def update_host(self, room: Room, session_id: str) -> None:
        room.host_session_id = session_id
        room.save(update_fields=["host_session_id"])


class ParticipantRepository:
    """Data access for Participant entities."""

    def create_host(self, room: Room, session_id: str, display_name: str) -> Participant:
        return Participant.objects.create(
            room=room,
            session_id=session_id,
            display_name=display_name,
            is_host=True,
        )

    def get_or_create(
        self,
        room: Room,
        session_id: str,
        display_name: str,
    ) -> tuple[Participant, bool]:
        participant, created = Participant.objects.get_or_create(
            room=room,
            session_id=session_id,
            defaults={"display_name": display_name},
        )
        if not created and participant.display_name != display_name:
            participant.display_name = display_name
            participant.save(update_fields=["display_name"])
        return participant, created

    def get_by_id(self, room: Room, participant_id: str) -> Participant:
        return get_object_or_404(Participant, id=participant_id, room=room)

    def clear_host_flags(self, room: Room) -> None:
        room.participants.filter(is_host=True).update(is_host=False)

    def promote_to_host(self, participant: Participant) -> None:
        participant.is_host = True
        participant.save(update_fields=["is_host"])


class QueueRepository:
    """Data access for QueueItem entities."""

    def create(
        self,
        room: Room,
        *,
        youtube_url: str,
        video_id: str,
        title: str,
        added_by_name: str,
        position: int,
    ) -> QueueItem:
        return QueueItem.objects.create(
            room=room,
            youtube_url=youtube_url,
            video_id=video_id,
            title=title,
            added_by_name=added_by_name,
            position=position,
        )

    def get_for_room(self, room: Room, item_id: str) -> QueueItem:
        return get_object_or_404(QueueItem, id=item_id, room=room)

    def has_playing_item(self, room: Room) -> bool:
        return room.queue_items.filter(status=QueueItem.Status.PLAYING).exists()

    def get_playing(self, room: Room) -> QueueItem | None:
        return room.queue_items.filter(status=QueueItem.Status.PLAYING).first()

    def get_next_queued(self, room: Room) -> QueueItem | None:
        return room.queue_items.filter(status=QueueItem.Status.QUEUED).order_by("position").first()

    def count(self, room: Room) -> int:
        return room.queue_items.count()

    def reorder_queued(self, room: Room) -> None:
        for idx, item in enumerate(
            room.queue_items.filter(status=QueueItem.Status.QUEUED).order_by("position")
        ):
            if item.position != idx:
                item.position = idx
                item.save(update_fields=["position"])

    def delete(self, item: QueueItem) -> None:
        item.delete()
