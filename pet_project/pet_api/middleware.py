from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from .urls import app_name as api_app_name


class HttpResponseUnauthorized(HttpResponse):
    """Custom API response for unauthorized requests."""
    status_code = 401
    default_content = 'I\'m sorry. Required parameters are missing or were not passed correctly.'

    def __init__(self, *args, **kwargs):
        super().__init__(content=self.default_content, *args, **kwargs)


class ApiAuthenticationMiddleware(MiddlewareMixin):
    """API Key Authentication."""

    def process_request(self, request):
        # Если это запрос к API - обязательно проверяем авторизационный ключ
        api_request = request.path.startswith(f'/{api_app_name}')
        valid_key = request.headers.get(settings.API_AUTH_HEADER) == settings.API_KEY
        if api_request and not valid_key:
            return HttpResponseUnauthorized()
