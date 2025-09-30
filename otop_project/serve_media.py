from django.http import FileResponse, Http404
from django.conf import settings
import os

def serve_media(request, path):
    """Serve media files manually"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        raise Http404(f"File not found: {path}")