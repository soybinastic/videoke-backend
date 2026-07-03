from django.urls import path

from rooms.api.views.queue_views import AddToQueueView, RemoveFromQueueView, SkipSongView
from rooms.api.views.reaction_views import SendApplauseView, SendReactionView
from rooms.api.views.room_views import CreateRoomView, JoinRoomView, RoomDetailView, TransferHostView

urlpatterns = [
    path("rooms/", CreateRoomView.as_view(), name="create-room"),
    path("rooms/<str:code>/", RoomDetailView.as_view(), name="get-room"),
    path("rooms/<str:code>/join/", JoinRoomView.as_view(), name="join-room"),
    path("rooms/<str:code>/transfer-host/", TransferHostView.as_view(), name="transfer-host"),
    path("rooms/<str:code>/queue/", AddToQueueView.as_view(), name="add-to-queue"),
    path(
        "rooms/<str:code>/queue/<uuid:item_id>/",
        RemoveFromQueueView.as_view(),
        name="remove-from-queue",
    ),
    path("rooms/<str:code>/skip/", SkipSongView.as_view(), name="skip-song"),
    path("rooms/<str:code>/reactions/", SendReactionView.as_view(), name="send-reaction"),
    path("rooms/<str:code>/applause/", SendApplauseView.as_view(), name="send-applause"),
]
