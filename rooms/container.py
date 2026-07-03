from rooms.parsers import get_video_url_parser
from rooms.repositories import ParticipantRepository, QueueRepository, RoomRepository
from rooms.services.broadcaster import ChannelsRoomEventBroadcaster
from rooms.services.queue_service import QueueService
from rooms.services.reaction_service import ReactionService
from rooms.services.room_service import RoomService


def get_room_service() -> RoomService:
    broadcaster = ChannelsRoomEventBroadcaster()
    return RoomService(
        room_repository=RoomRepository(),
        participant_repository=ParticipantRepository(),
        broadcaster=broadcaster,
    )


def get_queue_service() -> QueueService:
    return QueueService(
        room_repository=RoomRepository(),
        queue_repository=QueueRepository(),
        video_parser=get_video_url_parser(),
        broadcaster=ChannelsRoomEventBroadcaster(),
    )


def get_reaction_service() -> ReactionService:
    return ReactionService(
        room_repository=RoomRepository(),
        broadcaster=ChannelsRoomEventBroadcaster(),
    )
