from django.db import models


# ToDo: Rozważyć zrobienie name sali jako unique
class Room(models.Model):
    name = models.CharField(max_length=120)
    seats = models.IntegerField()
    has_projector = models.BooleanField()


class Booking(models.Model):
    date = models.DateField()
    comment = models.TextField(null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


