from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.http import HttpResponse
from .serve_media import serve_media 

schema_view = get_schema_view(
    openapi.Info(
        title="OTOP API",
        default_version='v1',
        description="API documentation for OTOP backend",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def home(request):
    return HttpResponse("OTOP API is running 🚀")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("otop_app.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", home, name="home"),
    re_path(r'^media/(?P<path>.*)$', serve_media, name='serve_media'),
]

# เสิร์ฟ media files
if settings.DEBUG:
    from django.views.static import serve
    
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
    
    print("🎉 MEDIA URL PATTERN HAS BEEN ADDED!")
    print(f"📂 Serving media from: {settings.MEDIA_ROOT}")