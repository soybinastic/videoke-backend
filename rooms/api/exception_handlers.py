from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from rooms.domain.exceptions import DomainError, HostPermissionError, InvalidReactionError


def domain_exception_handler(exc, context):
    """Map domain exceptions to HTTP responses."""
    if isinstance(exc, HostPermissionError):
        return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
    if isinstance(exc, InvalidReactionError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exc, DomainError):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    return exception_handler(exc, context)
