"""
WSGI config for MedResults project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
# import locale
# locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')
# print(locale.getlocale())
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MedResults.settings')

application = get_wsgi_application()
