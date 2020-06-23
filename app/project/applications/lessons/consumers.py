import os

from asgiref.sync import sync_to_async

from core.base import BaseConsumer, DjangoViewAsConsumer
from core.pagination import LimitOffsetPagination
from .models import Lesson
from .serializers import LessonSerializer
from project.utils.amqp_handlers import PikaProducerHandler


RABBIT_HOST = os.environ['RABBIT_HOST']
RABBIT_LOGIN = os.environ['RABBIT_LOGIN']
RABBIT_PASSWORD = os.environ['RABBIT_PASSWORD']

"""
# Не используется
class LessonConsumer(BaseConsumer):

    producer = PikaProducerHandler(
        connection_string=f'amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{RABBIT_HOST}:5672/%2F',
        queue_name='lesson_update_queue'
    )

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LimitOffsetPagination

    async def websocket_connect(self, message):
        await self.connect()
        await self.send("Send request to DB for outdated (maybe) data")
        resp_data, _ = await self.list()
        if self.paginator:
            paginated = await self.paginate_queryset(resp_data)
            resp_data = await self.get_paginated_response(paginated)
        await self.send_json(resp_data)
        signal_data = {
            'action': 'update',
            'channel_name': self.channel_name
        }
        await self.send("Send request via rabbitmq to integration server to update data in DB")
        await sync_to_async(self.producer.publish_message)(signal_data)
        await self.send("Now we are waiting for integration server for update data in DB")

    async def receive_json(self, content, **kwargs):
        data, resp = await self.list()
        await self.send_json({"data": data})

    async def refresh_complete(self, event):
        await self.send("Integration server updated data")
        await self.send("Send request to DB for fresh data")
        resp_data, _ = await self.list()
        if self.paginator:
            paginated = await self.paginate_queryset(resp_data)
            resp_data = await self.get_paginated_response(paginated)
        await self.send_json(resp_data)
        await self.send("Closing connection")
        await self.close()
"""


class LessonConsumerFromView(DjangoViewAsConsumer):
    producer = PikaProducerHandler(
        connection_string=f'amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{RABBIT_HOST}:5672/%2F',
        queue_name='lesson_update_queue'
    )
