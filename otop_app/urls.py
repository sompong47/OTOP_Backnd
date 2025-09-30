from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
app_name = "otop_api"

urlpatterns = [
    # Product
    path('api/products/', views.ProductListView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('api/products/<int:product_id>/reviews/', views.ProductReviewListCreateView.as_view(), name='product-review-list-create'),

    # Category
    path('api/categories/', views.CategoryListView.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', views.CategoryManageView.as_view(), name='category-manage'),

    # Order
    path('api/orders/', views.create_order, name='create-order'),
    path('api/orders/my-orders/', views.get_orders, name='get-orders'),
    path('api/orders/list/', views.OrderListView.as_view(), name='order-list'),
    path('api/orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('api/my-orders/', views.MyOrderListView.as_view(), name='my-order-list'),
    path('api/orders/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('orders/create/v2/', views.create_order_v2, name='create_order_v2'),

    # Seller
    path('api/seller/', views.SellerDetailView.as_view(), name='seller-detail'),
    path('api/seller/products/', views.SellerProductListView.as_view(), name='seller-product-list'),
    path('api/seller/products/<int:pk>/', views.ProductManageView.as_view(), name='seller-product-manage'),
    path('api/seller/orders/', views.SellerOrderListView.as_view(), name='seller-order-list'),
    path('api/seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),

    # User
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/profile/', views.UserProfileView.as_view(), name='user-profile'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]