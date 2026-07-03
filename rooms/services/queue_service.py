from uuid import UUID

from rooms.domain.constants import RoomEventType
from rooms.domain.host_guard import assert_is_host
from rooms.models import QueueItem, Room
from rooms.parsers.base import VideoUrlParser
from rooms.repositories import QueueRepository, RoomRepository
from rooms.serializers import QueueItemSerializer, RoomSerializer
from rooms.services.protocols import RoomEventBroadcaster


class QueueService:
    """Manages the song queue: add, remove, skip, and playback advancement."""

    def __init__(
        self,
        room_repository: RoomRepository,
        queue_repository: QueueRepository,
        video_parser: VideoUrlParser,
        broadcaster: RoomEventBroadcaster,
    ) -> None:
        self._rooms = room_repository
        self._queue = queue_repository
        self._parser = video_parser
        self._broadcaster = broadcaster

    def add_to_queue(
        self,
        code: str,
        session_id: str,
        youtube_url: str,
        added_by_name: str,
        title: str = "",
    ) -> dict:
        room = self._rooms.get_active_by_code(code)
        assert_is_host(room, session_id, "add songs to the queue")

        video_id = self._parser.extract_video_id(youtube_url)
        assert video_id is not None  # validated by serializer before service call

        item = self._queue.create(
            room,
            youtube_url=youtube_url,
            video_id=video_id,
            title=title or self._parser.default_title(video_id),
            added_by_name=added_by_name,
            position=self._queue.count(room),
        )

        if not self._queue.has_playing_item(room):
            self._advance_playback(room)

        self._broadcast_queue_update(room)
        return QueueItemSerializer(item).data

    def skip_song(self, code: str, session_id: str) -> dict:
        room = self._rooms.get_active_by_code(code)
        assert_is_host(room, session_id, "skip songs")

        self._advance_playback(room)
        state = self.serialize_room(room)
        self._broadcaster.broadcast(room.code, RoomEventType.QUEUE_UPDATED, state)
        self._broadcaster.broadcast(
            room.code,
            RoomEventType.SONG_SKIPPED,
            {"now_playing": state.get("now_playing")},
        )
        return state

    def remove_from_queue(self, code: str, item_id: UUID, session_id: str) -> dict:
        room = self._rooms.get_active_by_code(code)
        assert_is_host(room, session_id, "remove songs from the queue")

        item = self._queue.get_for_room(room, str(item_id))
        was_playing = item.status == QueueItem.Status.PLAYING
        self._queue.delete(item)

        if was_playing:
            self._advance_playback(room)

        self._queue.reorder_queued(room)
        self._broadcast_queue_update(room)
        return self.serialize_room(room)

    def _advance_playback(self, room: Room) -> QueueItem | None:
        current = self._queue.get_playing(room)
        if current:
            current.mark_done()

        next_item = self._queue.get_next_queued(room)
        if next_item:
            next_item.mark_playing()
        return next_item

    def _broadcast_queue_update(self, room: Room) -> None:
        self._broadcaster.broadcast(
            room.code,
            RoomEventType.QUEUE_UPDATED,
            self.serialize_room(room),
        )

    def serialize_room(self, room: Room) -> dict:
        return RoomSerializer(room).data
