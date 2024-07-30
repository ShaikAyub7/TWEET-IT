# custom_storages.py
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class DevelopmentStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.MEDIA_ROOT
        kwargs['base_url'] = settings.MEDIA_URL
        super().__init__(*args, **kwargs)

class ProductionStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        # Use a temporary directory for Vercel since it is read-only
        kwargs['location'] = '/tmp/media'
        kwargs['base_url'] = '/tmp/media/'
        super().__init__(*args, **kwargs)
