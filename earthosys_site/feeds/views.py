from django.shortcuts import render
from django.views import View
from .models import FeedPrediction
from .serializers import PredictorSerializer
from .serializers import FeedsSerializer
from predictor.models import PredictorRecord
from django.http import JsonResponse


class HomeView(View):
    def get(self, request):
        feeds, records, counter = {}, {}, 0
        predicted_feeds = FeedPrediction.objects.all().order_by('-id').values()[:5]
        feeds_serializer = FeedsSerializer(predicted_feeds, many=True)
        for feed in predicted_feeds:
            feeds[counter] = feed
            counter += 1
        counter = 0
        predictor_records = PredictorRecord.objects.all().order_by('-id').values()[:5]
        predictor_serializer = PredictorSerializer(predictor_records, many=True)
        for record in predictor_records:
            records[counter] = record
            counter += 1
        return JsonResponse({'feeds': feeds_serializer.data, 'records': predictor_serializer.data})
