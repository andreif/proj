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
        'jinja2',
        'psycopg2-binary',
        'requests',
        'dj-static',
        'django >= 2.2b1',
        'pywatchman',
        'raven',
        'gunicorn',
    ],
)
