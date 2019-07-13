import logging
import os
import sys
import threading

import django
from django.core import wsgi
from django.utils import timezone

from proj.settings import SRC_ROOT

sys.path.append(SRC_ROOT)

_local = threading.local()
_log = logging.getLogger(__name__)


def request_started():
    return getattr(_local, 'wsgi_request_started', None)


def request_ended():
    return getattr(_local, 'wsgi_request_ended', None)


def request_id():
    return getattr(_local, 'wsgi_request_id', None)


def request_duration():
    # _log.debug('Request %r duration', self.request_id())
    if request_started():
        delta = request_ended() - request_started()
        return delta.seconds + delta.microseconds / 1e6


def request_duration_str():
    s = request_duration()
    if s is None:
        return ''
    if s >= 1:
        return '%ds' % s
    ms = s * 1e3
    if ms >= 1:
        return '%dms' % ms
    return '%dus' % (ms * 1e3)


class WSGIHandler(wsgi.WSGIHandler):
    def get_response(self, request):
        _local.wsgi_request_started = timezone.now()
        _local.wsgi_request_id = id(request)
        _log.info('Request %d started: %s %s',
                  id(request), request.method, request.get_full_path())
        response = super().get_response(request=request)
        _local.wsgi_request_ended = timezone.now()
        _log.debug('Request %d ended in %s',
                   id(request), request_duration_str())
        return response


django.setup(set_prefix=False)
application = WSGIHandler()

# if os.environ.get('SENTRY_DSN'):
#     import sentry_sdk
#     from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
#     sentry_sdk.init()
#     application = SentryWsgiMiddleware(application)
