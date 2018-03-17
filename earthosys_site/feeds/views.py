from django.shortcuts import render
from django.views import View
from .models import FeedPrediction
from .serializers import PredictorSerializer
from .serializers import FeedsSerializer
from predictor.models import PredictorRecord
from django.http import JsonResponse


class HomeView(View):
    def get(self, request, id):
        if id == 0:
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
        elif id == 1:
            draw = request.GET['draw']
            start = int(request.GET['start'])
            length = int(request.GET['length'])
            predicted_feeds = FeedPrediction.objects.all().order_by('-id')[start: start + length].values()
            data = []
            for feed in predicted_feeds:
                data.append([feed[val] for val in feed])

            result = dict()
            result["data"] = data
            result["draw"] = draw
            result["recordsTotal"] = FeedPrediction.objects.count()
            result["recordsFiltered"] = FeedPrediction.objects.count()
            return JsonResponse(result)
