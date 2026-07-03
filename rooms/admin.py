from django.contrib import admin

from .models import Participant, QueueItem, Room

admin.site.register(Room)
admin.site.register(Participant)
admin.site.register(QueueItem)
