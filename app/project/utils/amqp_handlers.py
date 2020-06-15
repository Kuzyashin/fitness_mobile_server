import pika
import json


class PikaWorkerHandler:

    def __init__(self, connection_string, callback, main_queue_name,
                 consumer_tag='Worker', durable=True, auto_ack=False,
                 prefetch_count=1, redirect_result=False, result_queue_name=None
                 ):
        self._parameters = pika.URLParameters(connection_string)
        self._connection = None
        self._redirect_result = redirect_result
        self._channel_results = None
        self._main_queue_name = main_queue_name
        self._result_queue_name = result_queue_name
        self._callback = callback
        self._prefetch_count = prefetch_count
        self._auto_ack = auto_ack
        self._durable = durable
        self._consumer_tag = consumer_tag
        self._delivery_mode = 2 if durable else 1

    def _connect(self):
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        if self._redirect_result:
            self._channel_results = self._connection.channel()
            self._channel_results.queue_declare(queue=self._result_queue_name, durable=self._durable)
        self._channel.queue_declare(queue=self._main_queue_name, durable=self._durable)
        self._channel.basic_qos(prefetch_count=self._prefetch_count)


    def run_worker(self):
        try:
            self._connect()
            self._channel.basic_consume(
                on_message_callback=self._on_message, queue=self._main_queue_name, auto_ack=self._auto_ack,
                consumer_tag=self._consumer_tag
            )
            self._channel.start_consuming()
        except Exception:
            self._channel.stop_consuming()
            self._connection.close()
            self.run_worker()

    def publish_message_to_main(self, msg):
        self._connect()
        self._channel.basic_publish(
                exchange='', routing_key=self._main_queue_name,
                body=json.dumps(msg),
                properties=pika.BasicProperties(delivery_mode=self._delivery_mode)
        )

    def publish_message_to_result(self, msg):
        self._connect()
        self._channel.basic_publish(
                exchange='', routing_key=self._result_queue_name,
                body=json.dumps(msg),
                properties=pika.BasicProperties(delivery_mode=self._delivery_mode)
        )

    def _on_message(self, ch, method, properties, body):

        msg = body.decode()
        msg = json.loads(msg)
        self._callback(msg)
        if self._redirect_result:
            self.publish_message_to_result(
                {"action": "ready", "channel_name": msg.get("channel_name")}
            )
        if not self._auto_ack:
            ch.basic_ack(delivery_tag=method.delivery_tag)


class PikaProducerHandler:

    def __init__(self, connection_string, queue_name, durable=True):
        self._parameters = pika.URLParameters(connection_string)
        self._connection = None
        self._durable = durable
        self._queue_name = queue_name
        self._delivery_mode = 2 if durable else 1

    def _connect(self):
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name, durable=self._durable)

    def publish_message(self, msg):
        self._connect()
        self._channel.basic_publish(
                exchange='', routing_key=self._queue_name,
                body=json.dumps(msg),
                properties=pika.BasicProperties(delivery_mode=self._delivery_mode)
        )






"""worker = PikaWorkerHandler(
    connection_string='amqp://guest:guest@localhost:5672/%2F',
    callback=some_call,
    main_queue_name='lesson_update_queue',
    consumer_tag='Worker#1'
)

"""