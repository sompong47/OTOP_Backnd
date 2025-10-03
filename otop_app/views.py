from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import Product, Category, Order, Seller, ProductReview
from .serializers import (
    ProductSerializer, CategorySerializer, OrderSerializer, 
    CreateOrderSerializer, SellerSerializer, RegisterSerializer, 
    UserProfileSerializer, ProductReviewSerializer
)
import logging
import cloudinary.uploader  # ✅ import cloudinary

logger = logging.getLogger(__name__)

# ---------- Products ----------
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category','seller')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name','description','category__name']
    ordering_fields = ['price','created_at']
    permission_classes = [AllowAny]

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

# ---------- Categories ----------
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()

# ---------- Orders (เวอร์ชันเดิม) ----------
@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """สร้างออร์เดอร์ใหม่"""
    print(f"Create order request data: {request.data}")
    serializer = CreateOrderSerializer(data=request.data)
    
    if not serializer.is_valid():
        print(f"Order validation errors: {serializer.errors}")
        return Response({
            'success': False,
            'message': 'ข้อมูลไม่ถูกต้อง',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            items_data = serializer.validated_data['items']
            products_to_update = []
            
            for item in items_data:
                product = get_object_or_404(Product, id=item['product_id'])
                if product.stock < item['quantity']:
                    return Response({
                        'success': False,
                        'message': f'สินค้า "{product.name}" มีไม่เพียงพอ (เหลือ {product.stock} ชิ้น)'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                products_to_update.append({
                    'product': product,
                    'quantity': item['quantity']
                })
            
            # สร้างออร์เดอร์
            order = serializer.save()
            
            # ลด stock
            for item in products_to_update:
                product = item['product']
                product.stock -= item['quantity']
                product.save()
            
            # Serialize order เพื่อส่งข้อมูลเต็มกลับไป
            order_serializer = OrderSerializer(order)
            
            return Response({
                'success': True,
                'message': 'สั่งซื้อสำเร็จ',
                'data': order_serializer.data
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        print(f"Order creation error: {str(e)}")
        return Response({
            'success': False,
            'message': f'เกิดข้อผิดพลาด: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---------- Orders (เวอร์ชันใหม่ v2) ----------
@api_view(['POST'])
@permission_classes([AllowAny])
def create_order_v2(request):
    """สร้างออร์เดอร์ใหม่ (เวอร์ชัน v2 - return order data)"""
    try:
        order = Order.objects.create(
            customer_email=request.data.get('customer_email'),
            total_amount=request.data.get('total_amount', 0),
            status='pending'
        )
        
        return Response({
            'success': True,
            'message': 'Order created successfully',
            'data': {
                'id': order.id,
                'order_number': getattr(order, 'order_number', None),
                'status': order.status,
                'total': str(order.total_amount),
            }
        }, status=201)
    
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=400)

# ---------- Orders (อื่น ๆ) ----------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    try:
        orders = Order.objects.filter(customer_email=request.user.email).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'success': True,
            'orders': serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'ไม่สามารถดึงข้อมูลได้: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'seller'):
            return Order.objects.filter(items__product__seller=user.seller).distinct().order_by('-created_at')
        return Order.objects.filter(customer_email=user.email).order_by('-created_at')

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'seller'):
            return Order.objects.filter(items__product__seller=user.seller).distinct()
        return Order.objects.filter(customer_email=user.email)

class MyOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer_email=self.request.user.email).order_by('-created_at')

class OrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            order = get_object_or_404(Order, pk=pk)
            
            if not hasattr(request.user, 'seller') or not order.items.filter(product__seller=request.user.seller).exists():
                return Response({
                    'success': False,
                    'message': 'ไม่มีสิทธิ์แก้ไขออร์เดอร์นี้'
                }, status=status.HTTP_403_FORBIDDEN)
            
            status_value = request.data.get('status')
            if status_value not in dict(Order.STATUS_CHOICES):
                return Response({
                    'success': False,
                    'message': 'สถานะไม่ถูกต้อง'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            order.status = status_value
            order.save()
            
            return Response({
                'success': True,
                'message': 'อัพเดทสถานะสำเร็จ',
                'status': status_value
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'เกิดข้อผิดพลาด: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---------- Seller ----------
@api_view(['GET'])
def seller_dashboard(request):
    return Response({
        'success': True,
        'data': {
            'today_sales': 1500.0,
            'sales_growth': 5.2,
            'new_orders': 12,
            'pending_orders': 3,
            'total_products': 25,
            'low_stock_products': 2,
            'average_rating': 4.5,
            'total_reviews': 48,
            'recent_activities': [
                {
                    'type': 'order',
                    'title': 'คำสั่งซื้อใหม่',
                    'subtitle': 'มีคำสั่งซื้อใหม่ 3 รายการ',
                    'time': '5 นาทีที่แล้ว'
                }
            ]
        }
    })

class SellerDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Seller, user=self.request.user)

# ---------- Seller Products (แก้ไขให้รองรับ Cloudinary) ----------
class SellerProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller__user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        seller = get_object_or_404(Seller, user=self.request.user)

        # ✅ อัปโหลดรูปไป Cloudinary ก่อน save
        image_file = self.request.FILES.get('image')
        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="products/",
                use_filename=True,
                unique_filename=False
            )
            image_url = upload_result['secure_url']
            serializer.save(seller=seller, image=image_url)
        else:
            serializer.save(seller=seller)

class ProductManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller__user=self.request.user)

    def perform_update(self, serializer):
        image_file = self.request.FILES.get('image')
        if image_file:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="products/",
                use_filename=True,
                unique_filename=False
            )
            image_url = upload_result['secure_url']
            serializer.save(image=image_url)
        else:
            serializer.save()

class SellerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        seller = get_object_or_404(Seller, user=self.request.user)
        return Order.objects.filter(items__product__seller=seller).distinct().order_by('-created_at')

# ---------- Register & Profile ----------
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        print(f"📱 Register request headers: {dict(request.headers)}")
        print(f"📱 Register request data: {request.data}")
        print(f"📱 Register request content type: {request.content_type}")
        
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                print(f"❌ Register validation errors: {serializer.errors}")
                return Response({
                    'success': False,
                    'message': 'ข้อมูลไม่ถูกต้อง',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()
            print(f"✅ User created successfully: {user.username}")
            
            return Response({
                'success': True,
                'message': 'สมัครสมาชิกสำเร็จ',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"❌ Register error: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({
                'success': False,
                'message': f'สมัครสมาชิกไม่สำเร็จ: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# ---------- Product Review ----------
class ProductReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductReview.objects.filter(product_id=self.kwargs['product_id']).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs['product_id'])
        
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({
                'success': True,
                'message': 'เพิ่มรีวิวสำเร็จ',
                'review': response.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'เพิ่มรีวิวไม่สำเร็จ: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
