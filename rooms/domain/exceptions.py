"""Domain exceptions — raised by services, mapped to HTTP in the API layer."""


class DomainError(Exception):
    """Base class for domain-level errors."""


class HostPermissionError(DomainError):
    def __init__(self, message: str = "Only the host can perform this action.") -> None:
        super().__init__(message)


class InvalidReactionError(DomainError):
    def __init__(self, message: str = "Invalid reaction.") -> None:
        super().__init__(message)


class ParticipantNotFoundError(DomainError):
    def __init__(self, message: str = "Participant not found in this room.") -> None:
        super().__init__(message)
