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
        'dj-database-url',
        'Jinja2',
        'psycopg2',
        'pylibmc',
        'requests',
        'whitenoise',
        'Django',
        'pywatchman',
        'sentry-sdk',
        'gunicorn',
    ],
)
