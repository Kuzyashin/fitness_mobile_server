import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from lessons.consumers import LessonConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path('lessons', LessonConsumer),
            ]
        )
    ),
})
