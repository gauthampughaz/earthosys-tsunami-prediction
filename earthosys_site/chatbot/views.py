from django.http import JsonResponse
from django.views import View
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../earthosys-chatbot/")
print(sys.path)
from earthosys_bot import bot_response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class BotResponse(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        if not data['input']:
            return JsonResponse({'status': 'success', 'response': "Please enter a valid input."})
        try:
            _response = bot_response(data['input'])
            return JsonResponse({'status': 'success', 'response': _response})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'response': "Please try again."})
