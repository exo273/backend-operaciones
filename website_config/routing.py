"""
Routing de WebSocket para website_config.
Define las rutas de WebSocket para señalización digital.
"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/signage/$', consumers.SignageConsumer.as_asgi()),
]
