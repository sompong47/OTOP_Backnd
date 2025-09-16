from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse   # ✅ เพิ่ม import นี้

from otop_app import views

schema_view = get_schema_view(
   openapi.Info(
      title="OTOP API",
      default_version='v1',
      description="API documentation for OTOP backend",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# ✅ เพิ่มฟังก์ชัน home
def home(request):
    return HttpResponse("OTOP API is running 🚀")

urlpatterns = [
    path("", home, name="home"),   # ✅ root URL
    path("admin/", admin.site.urls),
    path("", include("otop_app.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/products/<int:product_id>/reviews/", views.ProductReviewListCreateView.as_view(), name="product-review-list-create"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
