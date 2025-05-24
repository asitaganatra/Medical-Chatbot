from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/training_status/$', consumers.TrainingConsumer.as_asgi()),
]