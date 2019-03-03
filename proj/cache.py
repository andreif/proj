import os
from django.core.cache.backends import memcached
from django.utils.functional import cached_property


class MemCachier(memcached.PyLibMCCache):
    @cached_property
    def _cache(self):
        return self._lib.Client(
            servers=os.environ['MEMCACHIER_SERVERS'].split(','),
            username=os.environ['MEMCACHIER_USERNAME'],
            password=os.environ['MEMCACHIER_PASSWORD'],
            behaviors=self._options,
            binary=True,
        )
