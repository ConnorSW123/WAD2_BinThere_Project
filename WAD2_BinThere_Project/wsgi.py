"""
WSGI config for WAD2_BinThere_Project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os # pragma: no cover

from django.core.wsgi import get_wsgi_application # pragma: no cover

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2_BinThere_Project.settings') # pragma: no cover

application = get_wsgi_application() # pragma: no cover
