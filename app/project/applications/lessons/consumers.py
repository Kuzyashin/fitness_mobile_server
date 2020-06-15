import os
from typing import Type

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.serializers import Serializer

from .models import Lesson
from .serializers import LessonSerializer
from project.utils.amqp_handlers import PikaProducerHandler


RABBIT_HOST = os.environ['RABBIT_HOST']
RABBIT_LOGIN = os.environ['RABBIT_LOGIN']
RABBIT_PASSWORD = os.environ['RABBIT_PASSWORD']


class BaseConsumer(AsyncJsonWebsocketConsumer):
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    queryset = None
    serializer_class = None

    def get_queryset(self, **kwargs) -> QuerySet:
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method." % self.__class__.__name__
        )
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    async def get_serializer(self, *args, **kwargs) -> Serializer:
        serializer_class = await self.get_serializer_class()
        kwargs["context"] = await self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    async def get_serializer_class(self, **kwargs) -> Type[Serializer]:
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )
        return self.serializer_class

    async def get_serializer_context(self, **kwargs):
        return {"scope": self.scope, "consumer": self}

    async def list(self, **kwargs):
        queryset = await database_sync_to_async(self.get_queryset)(**kwargs)
        serializer = await self.get_serializer(
            instance=queryset, many=True
        )
        return serializer.data, status.HTTP_200_OK


class LessonConsumer(BaseConsumer):

    producer = PikaProducerHandler(
        connection_string=f'amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{RABBIT_HOST}:5672/%2F',
        queue_name='lesson_update_queue'
    )

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    async def websocket_connect(self, message):
        await self.connect()
        await self.send("Send request to DB for outdated (maybe) data")
        data, _ = await self.list()
        await self.send(data)
        signal_data = {
            'action': 'update',
            'channel_name': self.channel_name
        }
        await self.send("Send request via rabbitmq to integration server to update data in DB")
        await sync_to_async(self.producer.publish_message)(signal_data)
        await self.send("Now we are waiting for integration server for update data in DB")

    async def receive_json(self, content, **kwargs):
        data, resp = await self.list()
        await self.send(data)

    async def refresh_complete(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        await self.send("Integration server updated data")
        await self.send("Send request to DB for fresh data")
        data, _ = await self.list()
        await self.send(data)
        await self.send("Closing connection")
        await self.close()
