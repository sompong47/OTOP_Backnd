from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI Schema
schema_view = get_schema_view(
    openapi.Info(
        title="OTOP Project API",
        default_version='v1',
        description="API documentation for OTOP Project",
        contact=openapi.Contact(email="support@otop.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Home Page
def home(request):
    return HttpResponse("🎉 ยินดีต้อนรับสู่ OTOP Project API 🎉")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),

    # API routes
    path('api/', include('otop_app.urls')),

    # Swagger Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
