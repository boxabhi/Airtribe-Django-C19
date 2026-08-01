"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from orders.consumers import OrderConsumer,JobConsumer
from django.urls import path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()

ws_patterns = [
    path("ws/orders/<str:order_id>/", OrderConsumer.as_asgi()),
    path("ws/job/<str:job_id>/", JobConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(ws_patterns),
})


# ws://127.0.0.1:8000/ws/orders/OD202607251/