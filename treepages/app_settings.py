import os
import django

FEINCMS_ADMIN_MEDIA = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'treepages/media/')
FEINCMS_ADMIN_MEDIA_HOTLINKING = False

# Whether Django 1.0 compatibilty mode should be active or not
DJANGO10_COMPAT = django.VERSION[0] < 1 or (django.VERSION[0] == 1 and django.VERSION[1] < 1)
