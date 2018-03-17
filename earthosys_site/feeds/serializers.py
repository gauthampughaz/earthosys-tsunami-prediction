from rest_framework import serializers
from predictor.models import PredictorRecord
from .models import FeedPrediction


class PredictorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictorRecord
        fields = ('magnitude', 'depth', 'latitude', 'longitude', 'date', 'tsunami', 'nearest_lat', 'nearest_lng', 'location', 'speed', 'distance')


class FeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedPrediction
        fields = ('magnitude', 'depth', 'latitude', 'longitude', 'date_time', 'tsunami', 'epicenter', 'nearest_lat', 'nearest_lng', 'location', 'speed', 'distance')