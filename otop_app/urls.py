from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "otop_api"  # Optional: ช่วย namespace URLs

urlpatterns = [
    # Product
    path('api/v1/products/', views.ProductListView.as_view(), name='product-list'),
    path('api/v1/products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('api/v1/products/<int:product_id>/reviews/', views.ProductReviewListCreateView.as_view(), name='product-review-list-create'),

    # Category
    path('api/v1/categories/', views.CategoryListView.as_view(), name='category-list'),
    path('api/v1/categories/<int:pk>/', views.CategoryManageView.as_view(), name='category-manage'),

    # Order
    path('api/v1/orders/', views.create_order, name='create-order'),
    path('api/v1/orders/list/', views.OrderListView.as_view(), name='order-list'),
    path('api/v1/orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('api/v1/my-orders/', views.MyOrderListView.as_view(), name='my-order-list'),
    path('api/v1/orders/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),

    # Seller
    path('api/v1/seller/', views.SellerDetailView.as_view(), name='seller-detail'),
    path('api/v1/seller/products/', views.SellerProductListView.as_view(), name='seller-product-list'),
    path('api/v1/seller/products/<int:pk>/', views.ProductManageView.as_view(), name='seller-product-manage'),
    path('api/v1/seller/orders/', views.SellerOrderListView.as_view(), name='seller-order-list'),

    # User
    path('api/v1/register/', views.RegisterView.as_view(), name='register'),
    path('api/v1/profile/', views.UserProfileView.as_view(), name='user-profile'),

    # JWT
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
