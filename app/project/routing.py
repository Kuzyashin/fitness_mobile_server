import os

from core.base import view_as_consumer
from lessons.views import LessonViewSet

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from lessons.consumers import LessonConsumerFromView

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path('lessons', view_as_consumer(LessonViewSet.as_view({'get': 'list'}), LessonConsumerFromView)),
            ]
        )
    ),
})
