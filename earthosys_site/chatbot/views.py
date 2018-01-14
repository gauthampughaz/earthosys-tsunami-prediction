from django.http import JsonResponse
import json
import sys
sys.path.append('/home/gautham/earthosys/earthosys-chatbot/')
from earthosys_bot import bot_response


# lAXu8NbVKX3R9IUmZjZuOrO4lfBSYEUsg3Vi3Ozr6hhkKZPzwrfyrnDo5YFeSIdu

def response(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        _response = bot_response(data['input'])
        return JsonResponse({'response': _response})


