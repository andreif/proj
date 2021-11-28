import logging

from django.template.defaultfilters import filesizeformat
from django.utils import log, termcolors

np = termcolors.PALETTES[termcolors.NOCOLOR_PALETTE]
lp = termcolors.PALETTES[termcolors.LIGHT_PALETTE]
dp = termcolors.PALETTES[termcolors.DARK_PALETTE]
lp['HTTP_SUCCESS']['opts'] = ('bold',)
dp['HTTP_SUCCESS']['opts'] = ('bold',)
np['INFO'] = {}
lp['INFO'] = dp['INFO'] = {'opts': ('bold',)}


class Formatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.style = log.color_style()
        super().__init__(*args, **kwargs)

    def format(self, record):
        from django.conf import settings
        repo_root = str(settings.REPO_ROOT) + '/'
        for x in ['/site-packages/', repo_root]:
            record.pathname = record.pathname.split(x)[-1]
        record.msg = record.msg.replace(repo_root, '')  # e.g. in autoreload
        clr = getattr(self.style, record.levelname, None)
        record.levelname = '%-7s' % record.levelname
        if clr:
            record.levelname = clr(record.levelname)
        return super().format(record)


class ServerFormatter(log.ServerFormatter):
    def format(self, record):
        import proj.wsgi
        record.size = record.proto = ''
        record.duration = proj.wsgi.request_duration_str()
        record.request_id = proj.wsgi.request_id()
        if len(record.args) == 3:
            a1, a2 = str(record.args[0]).rsplit(' ', 1)
            if a2 == 'HTTP/1.1':
                record.size = format_size(record.args[2])
                record.proto = a2
                record.msg = '%s'
                record.args = (a1,)
        return super().format(record)


def format_size(size):
    size = filesizeformat(size)
    size = size.replace('\xa0', '')
    return size.replace('byte', 'B')
