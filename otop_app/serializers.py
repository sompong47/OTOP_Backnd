from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Category, Seller, Order, OrderItem, ProductReview


# ---------------- Category ----------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# ---------------- Seller ----------------
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name', 'phone', 'is_verified']

# ---------------- Product ----------------
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.name', read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['seller']
    
    def to_representation(self, instance):
        """แปลง output ให้เหมาะกับ Flutter"""
        data = super().to_representation(instance)
        
        # เปลี่ยน category จาก ID เป็น name
        data['category'] = instance.category.name if instance.category else None
        
        # เปลี่ยน seller จาก ID เป็น name  
        data['seller'] = instance.seller.name if instance.seller else None
        
        # แปลง is_active เป็น is_available
        data['is_available'] = data.pop('is_active', True)
        
        # จัดการ image URL - ให้ full URL
        if instance.image:
            request = self.context.get('request')
            if request:
                data['image'] = request.build_absolute_uri(instance.image.url)
            else:
                # Fallback สำหรับกรณีไม่มี request context
                data['image'] = f"http://127.0.0.1:8000{instance.image.url}" if instance.image.url else None
        else:
            data['image'] = None
            
        return data

# ---------------- OrderItem ----------------
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'quantity', 'price']

class CreateOrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

# ---------------- Order ----------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','customer_name','customer_phone','customer_email','total_amount','shipping_address','payment_method','status','created_at','items']

class CreateOrderSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=200, default='Customer')
    customer_phone = serializers.CharField(max_length=20, required=False)
    customer_email = serializers.EmailField(required=False)
    shipping_address = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES)
    items = CreateOrderItemSerializer(many=True)

    def create(self, validated_data):
        print(f"Creating order with validated data: {validated_data}")
        items_data = validated_data.pop('items')
        total_amount = 0
        order_items = []

        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product_id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {item_data['product_id']} does not exist")
            quantity = item_data['quantity']
            price = float(item_data['price'])
            total_amount += price * quantity
            order_items.append({'product': product,'quantity': quantity,'price': price})

        order = Order.objects.create(total_amount=total_amount, **validated_data)
        for item_data in order_items:
            OrderItem.objects.create(order=order, **item_data)
        
        print(f"Order created successfully: {order.id}")
        return order

# ---------------- User ----------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['id','username','email','password']
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("ชื่อผู้ใช้นี้มีคนใช้แล้ว")
        return value
    
    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("อีเมลนี้มีคนใช้แล้ว")
        return value
    
    def create(self, validated_data):
        print(f"Creating user with validated data: {validated_data}")
        try:
            user = User.objects.create_user(
                username=validated_data['username'], 
                email=validated_data.get('email', ''), 
                password=validated_data['password']
            )
            print(f"User created successfully: {user.username}")
            return user
        except Exception as e:
            print(f"Error creating user: {e}")
            raise serializers.ValidationError(f"ไม่สามารถสร้างผู้ใช้ได้: {str(e)}")

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

# ---------------- ProductReview ----------------
class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']