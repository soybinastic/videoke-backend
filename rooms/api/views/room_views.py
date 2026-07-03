from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rooms.container import get_room_service
from rooms.serializers import CreateRoomSerializer, JoinRoomSerializer, TransferHostSerializer


class CreateRoomView(APIView):
    """POST /api/rooms/ — create a new karaoke room."""

    def post(self, request: Request) -> Response:
        serializer = CreateRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = get_room_service()
        room_state = service.create_room(
            name=data["name"],
            host_name=data["host_name"],
            session_id=data["session_id"],
        )
        return Response(room_state, status=status.HTTP_201_CREATED)


class RoomDetailView(APIView):
    """GET /api/rooms/{code}/ — fetch current room state."""

    def get(self, request: Request, code: str) -> Response:
        service = get_room_service()
        return Response(service.get_room(code))


class JoinRoomView(APIView):
    """POST /api/rooms/{code}/join/ — join an existing room."""

    def post(self, request: Request, code: str) -> Response:
        serializer = JoinRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = get_room_service()
        room_state = service.join_room(
            code=code,
            display_name=data["display_name"],
            session_id=data["session_id"],
        )
        return Response(room_state)


class TransferHostView(APIView):
    """POST /api/rooms/{code}/transfer-host/ — host transfers control to another participant."""

    def post(self, request: Request, code: str) -> Response:
        serializer = TransferHostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = get_room_service()
        room_state = service.transfer_host(
            code=code,
            session_id=data["session_id"],
            participant_id=data["participant_id"],
        )
        return Response(room_state)
