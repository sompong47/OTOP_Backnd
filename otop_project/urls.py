from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
import os

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
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("", include("otop_app.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# ✅ แก้ไขการ serve static และ media files
if settings.DEBUG or not os.environ.get('RAILWAY_ENVIRONMENT_NAME'):
    # Development mode - serve media and static files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug information
    print(f"📁 MEDIA_URL: {settings.MEDIA_URL}")
    print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"📁 Static files serving enabled for development")
    
    # Check if media directory exists
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        print(f"📁 Created MEDIA_ROOT directory: {settings.MEDIA_ROOT}")
    
    # Check specific product image
    product_image_path = os.path.join(settings.MEDIA_ROOT, 'products', 'homdang.png')
    if os.path.exists(product_image_path):
        print(f"✅ Product image found: {product_image_path}")
    else:
        print(f"❌ Product image NOT found: {product_image_path}")
        
        # List what's actually in the products directory
        products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        if os.path.exists(products_dir):
            files = os.listdir(products_dir)
            print(f"📋 Files in products directory: {files}")
        else:
            print(f"📋 Products directory doesn't exist: {products_dir}")