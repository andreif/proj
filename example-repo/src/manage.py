#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    assert os.environ.get('DJANGO_SETTINGS_MODULE') or '--settings=' in ''.join(sys.argv)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
