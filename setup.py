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
        'dj-database-url ==0.5.0',
        'Jinja2 ==2.10.1',
        'psycopg2-binary ==2.8.3',
        'requests ==2.22.0',
        'whitenoise ==4.1.2',
        'Django ==2.2.3',
        'pywatchman ==1.4.1',
        'sentry-sdk ==0.10.1',
        'gunicorn ==19.9.0',
    ],
)
