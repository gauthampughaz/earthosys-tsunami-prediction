from django.db import models
from datetime import datetime


class FeedPrediction(models.Model):
    REGION = (
        (1, 'Land'),
        (0, 'sea')
    )
    magnitude = models.FloatField()
    depth = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    epicenter = models.IntegerField(choices=REGION)
    date_time = models.DateTimeField(default=datetime.now, blank=True)
    tsunami = models.BooleanField()

    def __str__(self):
        return str([self.magnitude, self.depth, self.latitude, self.longitude, self.tsunami])
