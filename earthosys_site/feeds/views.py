from django.shortcuts import render
from django.views import View
from .models import FeedPrediction
from .serializers import PredictorSerializer
from .serializers import FeedsSerializer
from predictor.models import PredictorRecord
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name='dispatch')
class FeedsView(View):
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

    def post(self, request):
        json_data = json.loads(request.body.decode("utf-8"))
        draw = json_data['draw']
        start = int(json_data['start'])
        length = int(json_data['length'])
        predicted_feeds = FeedPrediction.objects.all().order_by('-id')[start: start + length].values()
        feeds_serializer = FeedsSerializer(predicted_feeds, many=True)

        result = dict()
        result["data"] = feeds_serializer.data
        result["draw"] = draw
        result["recordsTotal"] = FeedPrediction.objects.count()
        result["recordsFiltered"] = FeedPrediction.objects.count()
        return JsonResponse(result)
