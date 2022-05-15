#!/usr/bin/env python
from setuptools import setup, find_packages

version = __import__('proj').__version__

setup(
    name='proj',
    version=version,
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Jinja2',
        'psycopg2',
        'pylibmc',
        'requests',
        'whitenoise',
        'pywatchman',
        'sentry-sdk',
        'gunicorn',
        'Django',
        'dj-database-url',
        'django-cors-headers',
    ],
)
