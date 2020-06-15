from asgiref.sync import async_to_sync

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()


from utils.amqp_handlers import PikaWorkerHandler
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

RABBIT_HOST = os.environ['RABBIT_HOST']
RABBIT_LOGIN = os.environ['RABBIT_LOGIN']
RABBIT_PASSWORD = os.environ['RABBIT_PASSWORD']


def callback(msg):
    async_to_sync(channel_layer.send)(
        msg.get('channel_name'),
        {
            "data": "ready",
            "type": "refresh.complete"
        }
    )


worker = PikaWorkerHandler(
    connection_string=f'amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{RABBIT_HOST}:5672/%2F',
    callback=callback,
    main_queue_name='lesson_ready_queue',
    consumer_tag='Worker#1'
)

worker.run_worker()