"""
WSGI config for mona project.
"""
import os

from django.core.wsgi import get_wsgi_application

_dsm = os.environ.get('DJANGO_SETTINGS_MODULE', 'mona.settings.production')
# Railway ba'zan jip.settings.* deb auto-detect qiladi — buni override qilamiz
if _dsm.startswith('jip.'):
    _dsm = _dsm.replace('jip.', 'mona.', 1)
os.environ['DJANGO_SETTINGS_MODULE'] = _dsm

application = get_wsgi_application()

