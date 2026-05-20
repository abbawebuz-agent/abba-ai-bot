from django.urls import path

from .webhook import webhook_view

app_name = 'bot'

urlpatterns = [
    path('webhook/', webhook_view, name='webhook'),
]
