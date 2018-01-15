from django.views import View
from django.http import JsonResponse
from .forms import PredictorForm
from .models import PredictorRecord
import sys
sys.path.insert(0, '/home/gautham/earthosys/data_source/helper_modules/')
sys.path.insert(0, '/home/gautham/earthosys/earthosys-model/model/')
from data_processor import process_data
from tsunami_predictor import predict_tsunami


class PredictTsunamiView(View):
    form_class = PredictorForm
    template_name = '# template name goes here'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            record = PredictorRecord()
            record.magnitude = form.cleaned_data['magnitude']
            record.depth = form.cleaned_data['depth']
            record.latitude = form.cleaned_data['latitude']
            record.longitude = form.cleaned_data['longitude']

            input_ = process_data(input_data=[record.magnitude, record.depth, record.latitude, record.longitude])
            print(input_)
            record.tsunami = predict_tsunami([input_])
            record.save()
            if record.tsunami:
                return JsonResponse({'result': 'True', 'description': 'This is a tsunamigenic earthquake.'})
            else:
                return JsonResponse({'result': 'False', 'description': 'This is a non-tsunamigenic earthquake.'})


