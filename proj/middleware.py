import socket

from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware


class SystemInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for method in 'GET POST PUT DELETE'.split():
            setattr(request, 'is_' + method, request.method == method)
        response = self.get_response(request)
        response['X-App-Version'] = settings.VERSION
        response['X-App-Server'] = socket.gethostname()
        return response


class CustomSessionMiddleware(SessionMiddleware):
    def process_response(self, request, response):
        if request.path.lstrip('/').startswith(settings.ADMIN_URL):
            return super().process_response(request=request, response=response)
        return response
