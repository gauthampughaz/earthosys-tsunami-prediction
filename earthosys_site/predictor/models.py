from django.db import models
from datetime import datetime


class PredictorRecord(models.Model):
    magnitude = models.FloatField()
    depth = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    tsunami = models.BooleanField()
    nearest_lat = models.FloatField(default=None)
    nearest_lng = models.FloatField(default=None)
    distance = models.FloatField(default=None)
    location = models.CharField(max_length=1000, default="Location unavailable")
    speed = models.CharField(max_length=10, default="NA")

    def __str__(self):
        return str([self.magnitude, self. depth, self.latitude, self.longitude])
