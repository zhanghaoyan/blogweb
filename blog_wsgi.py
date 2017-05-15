#!/usr/local/python34/bin/python3
# coding: utf-8

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogweb.settings")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
