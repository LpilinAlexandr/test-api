from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class HttpResponseUnauthorized(HttpResponse):
    """Custom API response for unauthorized requests."""
    status_code = 401
    default_content = 'I\'m sorry. Required parameters are missing or were not passed correctly.'

    def __init__(self, *args, **kwargs):
        super().__init__(content=self.default_content, *args, **kwargs)


class ApiAuthenticationMiddleware(MiddlewareMixin):
    """API Key Authentication."""

    def process_request(self, request):
        if not request.headers.get(settings.API_AUTH_HEADER) == settings.API_KEY:
            return HttpResponseUnauthorized()
        return super().process_request(request)
