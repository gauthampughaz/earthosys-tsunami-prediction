from django.views import View
from django.http import JsonResponse
from .forms import PredictorForm
from .models import PredictorRecord
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import sys
import json
sys.path.insert(0, '/home/gautham/earthosys/data_source/helper_modules/')
sys.path.insert(0, '/home/gautham/earthosys/earthosys-model/model/')
from data_processor import process_data
from tsunami_predictor import predict_tsunami


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
            record.save()
            if record.tsunami:
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
