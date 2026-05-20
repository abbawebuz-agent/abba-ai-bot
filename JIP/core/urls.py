from django.http import JsonResponse
from django.urls import path

app_name = 'core'


def health(_request):
    return JsonResponse({'status': 'ok'})


def index(_request):
    return JsonResponse({
        'service': 'JIP Loyalty Platform',
        'status': 'running',
        'phase': 'Faza 1 — setup complete',
    })


urlpatterns = [
    path('', index, name='index'),
    path('health/', health, name='health'),
]
