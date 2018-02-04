from django.shortcuts import render
from django.views import View
from .models import FeedPrediction
from predictor.models import PredictorRecord
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class HomeView(View):
    def get(self, request):
        feeds, records, counter = {}, {}, 0
        predicted_feeds = FeedPrediction.objects.all().order_by('-id').values()[:5]
        for feed in predicted_feeds:
            feeds[counter] = feed
            counter += 1
        counter = 0
        predictor_records = PredictorRecord.objects.all().order_by('-id').values()[:5]
        for record in predictor_records:
            records[counter] = record
            counter += 1
        print(request.COOKIES)
        return JsonResponse({'feeds': feeds, 'records': records})
