from django.urls import re_path
from broadcaster import consumers

websocket_urlpatterns = [
    re_path(r'ws/announce/$', consumers.AnnounceConsumer.as_asgi()),
]
