from django.urls import re_path

from rooms.consumers.room_consumer import RoomConsumer

websocket_urlpatterns = [
    re_path(r"ws/rooms/(?P<code>[A-Za-z0-9]+)/$", RoomConsumer.as_asgi()),
]
