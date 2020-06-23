from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest




class WSRequest(HttpRequest):
    def _get_scheme(self):
        """
        Hook for subclasses like WSGIRequest to implement. Return 'http' by
        default.
        """
        return 'ws'

    @property
    def scheme(self):
        print(self.META)
        print(self.__dict__)
        if settings.SECURE_PROXY_SSL_HEADER:
            try:
                header, secure_value = settings.SECURE_PROXY_SSL_HEADER
            except ValueError:
                raise ImproperlyConfigured(
                    'The SECURE_PROXY_SSL_HEADER setting must be a tuple containing two values.'
                )
            header_value = self.META.get(header)
            if header_value is not None:
                return 'wss' if header_value == secure_value else 'ws'
        return self._get_scheme()
