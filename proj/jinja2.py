from django.conf import settings
from django.contrib.auth.context_processors import auth
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        # 'debug': settings.DEBUG,
    })
    return env
