from django.views import View
from django.http import JsonResponse
from .forms import PredictorForm
from .models import PredictorRecord
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import sys
import json
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../data_source/helper_modules/")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../earthosys_model/model/")
from data_processor import process_data
from data_processor import get_additional_info
from tsunami_predictor import predict_tsunami
from data_processor import alert_bot


@method_decorator(csrf_exempt, name='dispatch')
class PredictTsunamiView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        data = dict(map(lambda x: (x[0], float(x[1])), data.items()))
        if self.is_valid(data):
            record = PredictorRecord()
            record.magnitude = data["magnitude"]
            record.depth = data["depth"]
            record.latitude = data["latitude"]
            record.longitude = data['longitude']
            _input = process_data(input_data=[data["magnitude"], data["depth"], data["latitude"], data["longitude"]])
            record.tsunami = predict_tsunami([_input])
            addition_info = get_additional_info(record.latitude, record.longitude)
            record.nearest_lat = addition_info["nearest_lat"]
            record.nearest_lng = addition_info["nearest_lng"]
            record.location = addition_info["location"]
            record.distance = addition_info["distance"]
            record.speed = addition_info["speed"]
            record.save()
            if record.tsunami:
                alert_bot()
                return JsonResponse({'status': 'success', 'result': 'True', 'description': 'This is a tsunamigenic earthquake.'})
            else:
                return JsonResponse({'status': 'success', 'result': 'False', 'description': 'This is a non-tsunamigenic earthquake.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Please provide valid information for prediction.'})

    def is_valid(self, data):
        if not 0 < data["magnitude"] <= 10:
            return False
        elif not data["depth"] > 0:
            return False
        elif not -90 < data["latitude"] < 90:
            return False
        elif not -180 < data["longitude"] < 180:
            return False
        return True
