"""
ASGI config for operations_service project.
Configuración para soportar HTTP y WebSocket (Django Channels).
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import website_config.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'operations_service.settings')

# Inicializar Django ASGI application primero para configurar Django
django_asgi_app = get_asgi_application()

# Configurar el router de protocolos para HTTP y WebSocket
application = ProtocolTypeRouter({
    # HTTP tradicional
    "http": django_asgi_app,
    
    # WebSocket para señalización digital
    "websocket": AuthMiddlewareStack(
        URLRouter(
            website_config.routing.websocket_urlpatterns
        )
    ),
})
