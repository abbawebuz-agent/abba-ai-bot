from django.http import JsonResponse
from django.urls import path

app_name = 'core'


def health(_request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('health/', health, name='health'),
]
