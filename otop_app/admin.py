from django.contrib import admin
from .models import Category, Seller, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['name', 'phone']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'seller', 'price', 'stock', 'is_active']
    list_filter = ['category', 'seller', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['customer_name', 'customer_phone']
    list_editable = ['status']
    inlines = [OrderItemInline]