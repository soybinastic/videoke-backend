from rooms.domain.exceptions import HostPermissionError
from rooms.models import Room


def assert_is_host(room: Room, session_id: str, action: str = "perform this action") -> None:
    """Raise if the session does not belong to the current room host."""
    if not room.is_host(session_id):
        raise HostPermissionError(f"Only the host can {action}.")
