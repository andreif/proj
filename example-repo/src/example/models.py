from django.db import models as m


class _Model(m.Model):
    created_at = m.DateTimeField(auto_created=True, auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class Example(_Model):
#     content = m.TextField(null=True)
