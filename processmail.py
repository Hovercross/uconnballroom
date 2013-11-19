#!/usr/bin/env python

from ballroom import settings
from django.core.management import setup_environ
setup_environ(settings)

import sys

from mailhandler import lib

data = sys.stdin.read()

lib.processMessage(data)