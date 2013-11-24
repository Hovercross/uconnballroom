#! /var/www/uconnballroom.com/env/bin/python
import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ballroom.settings")

from mailhandler import lib
data = sys.stdin.read()
lib.processMessage(data)
