import socket
from django.conf import settings


class SystemInfoMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-App-Version'] = settings.VERSION
        response['X-App-Server'] = socket.gethostname()
        return response
