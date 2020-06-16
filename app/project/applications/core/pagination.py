"""
Pagination serializers determine the structure of the output that should
be used for paginated responses.
"""
from collections import OrderedDict
from urllib import parse

from rest_framework.settings import api_settings
from rest_framework.utils.urls import remove_query_param, replace_query_param


def _positive_int(integer_string, strict=False, cutoff=None):
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        return min(ret, cutoff)
    return ret


class BasePagination:
    def paginate_queryset(self, queryset, request, view=None):  # pragma: no cover
        raise NotImplementedError('paginate_queryset() must be implemented.')

    def get_paginated_response(self, data):  # pragma: no cover
        raise NotImplementedError('get_paginated_response() must be implemented.')

    def get_results(self, data):
        return data['results']


class LimitOffsetPagination(BasePagination):
    default_limit = api_settings.PAGE_SIZE or 50
    limit_query_param = 'limit'
    limit_query_description = 'Number of results to return per page.'
    offset_query_param = 'offset'
    offset_query_description = 'The initial index from which to return the results.'
    max_limit = None

    async def paginate_queryset(self, queryset, request, view=None):
        self.count = await self.get_count(queryset)
        self.limit = await self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = await self.get_offset(request)
        self.request = request

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset:self.offset + self.limit])

    async def get_paginated_response(self, data):
        return OrderedDict([
            ('count', self.count),
            ('next',  self.get_next_link()),
            ('previous',  self.get_previous_link()),
            ('results', data)
        ])

    async def get_limit(self, request):
        if self.limit_query_param:
            qs = parse.parse_qs(request['query_string'].decode())
            try:
                return _positive_int(
                    qs[self.limit_query_param][0],
                    strict=True,
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError):
                pass

        return self.default_limit

    async def get_offset(self, request):
        try:
            qs = parse.parse_qs(request['query_string'].decode())
            return _positive_int(
                qs[self.offset_query_param][0],
            )
        except (KeyError, ValueError):
            return 0

    def build_absolute_uri(self):
        path = self.request['path']
        host = self.request['headers'][0][1].decode()
        return f'wss://{host}{path}'

    def get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None

        url = self.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_previous_link(self):
        if self.offset <= 0:
            return None

        url = self.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        if self.offset - self.limit <= 0:
            return remove_query_param(url, self.offset_query_param)

        offset = self.offset - self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    async def get_count(self, queryset):
        """
        Determine an object count, supporting either querysets or regular lists.
        """
        try:
            return queryset.count()
        except (AttributeError, TypeError):
            return len(queryset)