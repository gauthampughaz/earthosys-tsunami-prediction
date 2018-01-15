from django.http import JsonResponse
from django.views import View
import json
import sys
sys.path.append('/home/gautham/earthosys/earthosys-chatbot/')
from earthosys_bot import bot_response


# FYM5pN9EGfnsogen3BaCdYxgAB49NaE3qCMfpnNN9CgadLI6TvsSgJHyJF1IQgJ2

class BotResponse(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        _response = bot_response(data['input'])
        return JsonResponse({'response': _response})


