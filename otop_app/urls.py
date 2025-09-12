from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Product
    path('api/products/', views.ProductListView.as_view()),
    path('api/products/<int:pk>/', views.ProductDetailView.as_view()),
    path('api/products/<int:product_id>/reviews/', views.ProductReviewListCreateView.as_view()),

    # Category
    path('api/categories/', views.CategoryListView.as_view()),
    path('api/categories/<int:pk>/', views.CategoryManageView.as_view()),

    # Order
    path('api/orders/', views.create_order),
    path('api/orders/list/', views.OrderListView.as_view()),
    path('api/orders/<int:pk>/', views.OrderDetailView.as_view()),
    path('api/my-orders/', views.MyOrderListView.as_view()),
    path('api/orders/<int:pk>/status/', views.OrderStatusUpdateView.as_view()),

    # Seller
    path('api/seller/', views.SellerDetailView.as_view()),
    path('api/seller/products/', views.SellerProductListView.as_view()),
    path('api/seller/products/<int:pk>/', views.ProductManageView.as_view()),
    path('api/seller/orders/', views.SellerOrderListView.as_view()),

    # User
    path('api/register/', views.RegisterView.as_view()),
    path('api/profile/', views.UserProfileView.as_view()),

    # JWT
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
