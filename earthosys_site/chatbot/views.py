from django.http import JsonResponse
from django.views import View
import json
import sys
sys.path.append('/home/gautham/earthosys/earthosys-chatbot/')
from earthosys_bot import bot_response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class BotResponse(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        _response = bot_response(data['input'])
        return JsonResponse({'response': _response})


