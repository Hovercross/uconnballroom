#!/usr/bin/env python

from ballroomcms import settings_development
from django.core.management import setup_environ
setup_environ(settings_development)

import sys

from mailhandler import lib

data = sys.stdin.read()

lib.processMessage(data)