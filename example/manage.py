#!/usr/bin/env python
import os
import sys


PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__))
)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
