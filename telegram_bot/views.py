import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .webhooks import process_telegram_update


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        update = json.loads(request.body)
        process_telegram_update(update)
        return HttpResponse(status=200)
    return JsonResponse({'status': 'error'}, status=400)
