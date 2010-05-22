#!/usr/bin/env python

"""
    Arista WSGI Server
    ====================
    Run the Arista website server through WSGI to a web server such
    as Apache or Lighty.
    
    See http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango
"""

import os
import sys

# Set the path to settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'arista-website.settings'

BASE = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.dirname(BASE))

# Path to where Django is
sys.path.insert(0, os.path.join(BASE, "contrib"))
for path in os.listdir(os.path.join(BASE, "contrib")):
    sys.path.insert(1, os.path.join(BASE, "contrib", path))

# Arista site base path so local imports work
sys.path.insert(0, BASE)

# Start handling requests
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

