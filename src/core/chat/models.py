from django.db import models

from auth_core.models import CustomUser

class TrackingModel(models.Model):
    created_on = models.DateTimeField('created_on', auto_now_add=True)
    updated_on = models.DateTimeField('updated_on', auto_now=True)

    class Meta:
        abstract = True


class Room(TrackingModel):
    room_name = models.CharField('room_name', max_length=150)
    owner = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    room_status = models.CharField('room_status', max_length=20)

    def __str__(self) -> str:
        return f'Room(room_name={self.room_name}, owner_id={self.owner_id}, room_status={self.room_status})'