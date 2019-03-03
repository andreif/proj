from typing import Optional, Union

from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html


def admin_url(instance: Union[models.Model, tuple]):
    if isinstance(instance, tuple):
        if len(instance) == 2:
            return reverse('admin:%s_%s_changelist' % instance)
        app, model, pk = instance
    else:
        app, model, pk = (instance._meta.app_label,
                          instance._meta.model_name,
                          instance.pk)
    url_name = 'admin:%s_%s_change' % (app, model)
    return reverse(url_name, args=(pk,))


def admin_link(instance: Union[models.Model, tuple],
               text: Optional[str] = None,
               query: Optional[str] = None):
    if not instance:
        return
    if callable(text):
        text = text(instance)
    if not text:
        text = instance
        if isinstance(text, tuple):
            text = text[-1]
    return format_html('<a href="{url}" class="changelink">{text}</a>',
                       url=admin_url(instance) + (query or ''),
                       text=text)


class ReadOnlyMixin:
    def get_readonly_fields(self, request, obj=None):
        assert isinstance(self, admin.ModelAdmin)
        meta = self.model._meta
        fields = list(self.fields or []) + \
            [f.name for f in meta.fields]
        _id = meta.pk.name
        fields = [_id] + list({f: f for f in fields if f != _id}.keys())
        return fields + list(self.readonly_fields or [])

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def setattrs(**kwargs):
    """
    A decorator allowing to set attributes on functions, handy for
    setting attrs on Django model admin methods, e.g. allow_tags,
    admin_order_field, short_description.
    """

    def wrapper(f):
        for k, v in kwargs.items():
            setattr(f, k, v)
        return f

    return wrapper
