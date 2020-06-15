from django.db import models

# Create your models here.


class Lesson(models.Model):
    name = models.CharField(
        max_length=255, null=True, blank=True
    )
    description = models.TextField(
        null=True, blank=True
    )
    place = models.CharField(
        max_length=255, null=True, blank=True
    )
    coach_id = models.UUIDField(
        null=True, blank=True
    )
    startTime = models.TimeField(
        null=True, blank=True
    )
    endTime = models.TimeField(
        null=True, blank=True
    )
    date = models.DateField(
        null=True, blank=True
    )
    appointment_id = models.UUIDField(
        null=True, blank=True
    )
    service_id = models.UUIDField(
        null=True, blank=True
    )
    available_slots = models.IntegerField(
        null=True, blank=True
    )
    commercial = models.BooleanField(
        default=False
    )
    client_recorded = models.BooleanField(
        default=False
    )
    tab = models.CharField(
        max_length=255, null=True, blank=True
    )
    color = models.CharField(
        max_length=255, null=True, blank=True
    )
    tab_id = models.IntegerField(
        null=True, blank=True
    )
