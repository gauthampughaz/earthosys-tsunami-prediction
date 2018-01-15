from django.db import models
from datetime import datetime


class PredictorRecord(models.Model):
    magnitude = models.FloatField()
    depth = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    tsunami = models.BooleanField()

    def __str__(self):
        return str([self.magnitude, self. depth, self.latitude, self.longitude])
