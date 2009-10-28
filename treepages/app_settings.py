import os
import django

TREEPAGES_PAGE_TEMPLATE_CHOICES = [
        ('treepages/pages/base.html', 'Base'),
        ('treepages/pages/segreteria.html','Segreteria*'),
        ('treepages/pages/areaDidattica.html','Area Didattica*'),
        ('treepages/pages/princNavaCentro.html','Principale Nava/Centro*'),
        ('treepages/pages/princCometa.html','Principale La Cometa*'),
        ('treepages/pages/princRonco.html','Principale Ronco*'),
        ('treepages/pages/princFrecciaAzzurra.html','Principale La Freccia Azzurra*')
        ]# Asterisk to signal templates with their own contents: text and attachments may appear if/where included by template author.

FEINCMS_ADMIN_MEDIA = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'treepages/media/')
FEINCMS_ADMIN_MEDIA_HOTLINKING = False

# Whether Django 1.0 compatibilty mode should be active or not
DJANGO10_COMPAT = django.VERSION[0] < 1 or (django.VERSION[0] == 1 and django.VERSION[1] < 1)
