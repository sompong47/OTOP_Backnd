from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status, filters, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import Product, Category, Order, Seller, ProductReview
from .serializers import (
    ProductSerializer, CategorySerializer, OrderSerializer, 
    CreateOrderSerializer, SellerSerializer, RegisterSerializer, 
    UserProfileSerializer, ProductReviewSerializer
)

# ---------- Products ----------
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category','seller')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name','description','category__name']
    ordering_fields = ['price','created_at']

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

# ---------- Categories ----------
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()

# ---------- Orders ----------
@api_view(['GET','POST'])
def create_order(request):
    if request.method == 'POST':
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # ตรวจสอบ stock
                for item in serializer.validated_data['items']:
                    product = get_object_or_404(Product, id=item['product_id'])
                    if product.stock < item['quantity']:
                        return Response({"error": f"สินค้ามีไม่พอ: {product.name}"}, status=status.HTTP_400_BAD_REQUEST)
                order = serializer.save()
                # ลด stock
                for item in order.items.all():
                    product = item.product
                    product.stock -= item.quantity
                    product.save()
                return Response({'message':'สั่งซื้อสำเร็จ','order_id':order.id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        if request.user.is_authenticated:
            orders = Order.objects.filter(customer_email=request.user.email)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        return Response({"error":"กรุณา login ก่อน"}, status=status.HTTP_401_UNAUTHORIZED)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'seller'):
            return Order.objects.filter(items__product__seller=user.seller).distinct()
        return Order.objects.filter(customer_email=user.email)

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
        return Order.objects.filter(customer_email=self.request.user.email)

class OrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if not hasattr(request.user, 'seller') or not order.items.filter(product__seller=request.user.seller).exists():
            return Response({'error':'No permission'}, status=403)
        status_value = request.data.get('status')
        if status_value not in dict(Order.STATUS_CHOICES):
            return Response({'error':'Invalid status'}, status=400)
        order.status = status_value
        order.save()
        return Response({'status':'updated'})

# ---------- Seller ----------
class SellerDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Seller, user=self.request.user)

class SellerProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller__user=self.request.user)

    def perform_create(self, serializer):
        seller = get_object_or_404(Seller, user=self.request.user)
        serializer.save(seller=seller)

class ProductManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller__user=self.request.user)

class SellerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        seller = get_object_or_404(Seller, user=self.request.user)
        return Order.objects.filter(items__product__seller=seller).distinct()

# ---------- Register & Profile ----------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

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
        return ProductReview.objects.filter(product_id=self.kwargs['product_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs['product_id'])
