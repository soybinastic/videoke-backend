from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rooms.container import get_reaction_service


class SendReactionView(APIView):
    """POST /api/rooms/{code}/reactions/ — broadcast a live emoji reaction."""

    def post(self, request: Request, code: str) -> Response:
        emoji = request.data.get("emoji", "")
        sender = request.data.get("sender", "Someone")

        service = get_reaction_service()
        service.send_reaction(code, emoji, sender)
        return Response({"ok": True})


class SendApplauseView(APIView):
    """POST /api/rooms/{code}/applause/ — trigger virtual applause."""

    def post(self, request: Request, code: str) -> Response:
        sender = request.data.get("sender", "Someone")

        service = get_reaction_service()
        service.send_applause(code, sender)
        return Response({"ok": True})
