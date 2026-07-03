from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rooms.container import get_queue_service
from rooms.serializers import AddQueueItemSerializer


class AddToQueueView(APIView):
    """POST /api/rooms/{code}/queue/ — add a YouTube song to the queue."""

    def post(self, request: Request, code: str) -> Response:
        serializer = AddQueueItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = get_queue_service()
        item = service.add_to_queue(
            code=code,
            session_id=data["session_id"],
            youtube_url=data["youtube_url"],
            added_by_name=data["added_by_name"],
            title=data.get("title", ""),
        )
        return Response(item, status=status.HTTP_201_CREATED)


class SkipSongView(APIView):
    """POST /api/rooms/{code}/skip/ — host skips the current song."""

    def post(self, request: Request, code: str) -> Response:
        session_id = request.data.get("session_id", "")
        service = get_queue_service()
        state = service.skip_song(code, session_id)
        return Response(state)


class RemoveFromQueueView(APIView):
    """DELETE /api/rooms/{code}/queue/{item_id}/ — remove a song from the queue."""

    def delete(self, request: Request, code: str, item_id: str) -> Response:
        session_id = request.data.get("session_id", "")
        service = get_queue_service()
        state = service.remove_from_queue(code, item_id, session_id)
        return Response(state)
