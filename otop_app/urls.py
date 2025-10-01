from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "otop_api"

urlpatterns = [
    # Product
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/reviews/', views.ProductReviewListCreateView.as_view(), name='product-review-list-create'),

    # Category
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryManageView.as_view(), name='category-manage'),


    
    # Order
path('orders/', views.OrderListView.as_view(), name='order-list'),  # ✅ GET list
path('orders/create/', views.create_order, name='create-order'),    # ✅ POST create
path('orders/create/v2/', views.create_order_v2, name='create_order_v2'),
path('orders/my-orders/', views.get_orders, name='get-orders'),
path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
path('orders/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),
path('my-orders/', views.MyOrderListView.as_view(), name='my-order-list'),

    # Seller
    path('seller/', views.SellerDetailView.as_view(), name='seller-detail'),
    path('seller/products/', views.SellerProductListView.as_view(), name='seller-product-list'),
    path('seller/products/<int:pk>/', views.ProductManageView.as_view(), name='seller-product-manage'),
    path('seller/orders/', views.SellerOrderListView.as_view(), name='seller-order-list'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),

    # User
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),

    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]