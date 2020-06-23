import json
import os
from typing import Type

import typing
from urllib import parse

from asgiref.sync import sync_to_async
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from core.http import WSRequest


class BaseConsumer(AsyncJsonWebsocketConsumer):
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    queryset = None
    serializer_class = None
    pagination_class = None

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

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.scope, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class DjangoViewAsConsumer(BaseConsumer):
    view = None
    producer = None

    def get_querydict(self, request):
        print(self.scope)
        query_string = self.scope.get('query_string', None).decode()
        query_dict = dict(parse.parse_qsl(query_string))
        return query_dict

    def get_server_name_port(self):
        server_host = self.scope.get('server')[0]
        server_port = self.scope.get('server')[1]
        print(dict(self.scope.get('headers')))
        print(dict(self.scope.get('headers').decode()))
        server_name = dict(self.scope.get('headers')).get('host')
        if server_name:
            return server_name, server_port
        else:
            return server_host, server_port

    @database_sync_to_async
    def call_view(self, action: str, **kwargs):
        request = WSRequest()
        request.path = self.scope.get("path")
        request.session = self.scope.get("session", None)
        request.query_params = self.get_querydict(request)

        request.META['HTTP_X_FORWARDED_HOST'] = dict(self.scope.get('headers')).get('host')
        request.META['SERVER_NAME'], request.META['SERVER_PORT'] = self.get_server_name_port()
        request.META["HTTP_CONTENT_TYPE"] = "application/json"
        request.META["HTTP_ACCEPT"] = "application/json"
        request.META["QUERY_STRING"] = self.scope.get('query_string', None).decode()
        request.GET = QueryDict(self.scope.get('query_string', None).decode())

        for (header_name, value) in self.scope.get("headers", []):
            request.META[header_name.decode("utf-8")] = value.decode("utf-8")

        request.method = 'get'
        request.POST = json.dumps(kwargs.get("data", {}))
        if self.scope.get("cookies"):
            request.COOKIES = self.scope.get("cookies")

        view = getattr(self.__class__, "view")
        response = view(request)

        status = response.status_code

        if isinstance(response, Response):
            data = response.data
            try:
                json.dumps(data)
                return data, status
            except Exception as e:
                pass

        response_content = response.content
        if isinstance(response_content, bytes):
            try:
                response_content = response_content.decode("utf-8")
            except Exception as e:
                response_content = response_content.hex()
        return response_content, status

    async def websocket_connect(self, message):
        await self.connect()
        await self.send("Send request to DB for outdated (maybe) data")
        data, _ = await self.call_view('list')
        await self.send_json(data)
        signal_data = {
            'action': 'update',
            'channel_name': self.channel_name
        }
        await self.send("Send request via rabbitmq to integration server to update data in DB")
        await sync_to_async(self.producer.publish_message)(signal_data)
        await self.send("Now we are waiting for integration server for update data in DB")

    async def refresh_complete(self, event):
        await self.send("Integration server updated data")
        await self.send("Send request to DB for fresh data")
        resp_data, _ = await self.call_view('list')
        await self.send_json(resp_data)
        await self.send("Closing connection")
        await self.close()


def view_as_consumer(
    wrapped_view: typing.Callable[[HttpRequest], HttpResponse],
    consumer: Type[AsyncConsumer] = DjangoViewAsConsumer,
) -> Type[AsyncConsumer]:

    class DjangoViewWrapper(consumer):
        view = wrapped_view

    return DjangoViewWrapper
