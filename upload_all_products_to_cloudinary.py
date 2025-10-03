"""
upload_products_railway.py
รันบน Railway เพื่ออัปโหลดรูปไป Cloudinary และอัปเดต PostgreSQL
"""

import os
import django
import cloudinary
import cloudinary.uploader
from django.conf import settings

# ---------------------------
# ตั้งค่า Django
# ---------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "otop_project.settings")
django.setup()

from otop_app.models import Product

# ---------------------------
# ตั้งค่า Cloudinary (บังคับใช้)
# ---------------------------
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    print("❌ กรุณาตั้งค่า Environment Variables สำหรับ Cloudinary")
    print("   - CLOUDINARY_CLOUD_NAME")
    print("   - CLOUDINARY_API_KEY")
    print("   - CLOUDINARY_API_SECRET")
    exit(1)

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

print("=" * 70)
print("🚀 เริ่มอัปโหลดรูปภาพไป Cloudinary (Railway)")
print("=" * 70)
print(f"☁️  Cloudinary: {CLOUDINARY_CLOUD_NAME}")
print(f"📊 Database: PostgreSQL (Railway)")
print("=" * 70)

# ---------------------------
# ดึงสินค้าทั้งหมด
# ---------------------------
products = Product.objects.all()

if not products.exists():
    print("⚠️  ไม่มีสินค้าในฐานข้อมูล")
    exit(0)

success_count = 0
skip_count = 0
error_count = 0
no_image_count = 0

for product in products:
    print(f"\n📦 Product {product.id}: {product.name}")
    
    if not product.image:
        print(f"   ℹ️  ไม่มีรูป - ข้าม")
        no_image_count += 1
        continue

    image_str = str(product.image)
    print(f"   📷 Image ปัจจุบัน: {image_str}")

    # เช็คว่าเป็น Cloudinary URL อยู่แล้วหรือไม่
    if "cloudinary.com" in image_str or "res.cloudinary.com" in image_str:
        print(f"   ✅ มี Cloudinary URL อยู่แล้ว")
        skip_count += 1
        continue

    # กรณีเป็น Local path หรือ Media URL
    # ถ้ารูปอยู่ใน Railway แล้ว ก็ไม่มีไฟล์จริงให้อัปโหลด
    # ต้องใช้ URL ที่มีอยู่หรืออัปโหลดจาก URL
    
    if image_str.startswith('http://') or image_str.startswith('https://'):
        # ถ้าเป็น URL แล้ว ให้อัปโหลดจาก URL
        try:
            print(f"   ⬆️  กำลังอัปโหลดจาก URL...")
            result = cloudinary.uploader.upload(
                image_str,
                folder="otop_products",
                public_id=f"product_{product.id}",
                overwrite=True,
                resource_type="image"
            )
            
            secure_url = result['secure_url']
            product.image = secure_url
            product.save()
            
            print(f"   ✅ สำเร็จ!")
            print(f"   🔗 URL ใหม่: {secure_url}")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ อัปโหลดล้มเหลว: {str(e)}")
            error_count += 1
    else:
        # กรณีเป็น path ที่ไม่มีไฟล์จริง
        print(f"   ⚠️  ไม่สามารถอัปโหลด Local path บน Railway ได้")
        print(f"   💡 กรุณาอัปโหลดรูปใหม่ผ่าน Admin หรือ API")
        error_count += 1

# ---------------------------
# สรุปผลลัพธ์
# ---------------------------
print("\n" + "=" * 70)
print("📊 สรุปผลการอัปโหลด")
print("=" * 70)
print(f"✅ สำเร็จ: {success_count} รายการ")
print(f"⏭️  ข้าม (มี Cloudinary URL): {skip_count} รายการ")
print(f"ℹ️  ไม่มีรูป: {no_image_count} รายการ")
print(f"❌ ล้มเหลว: {error_count} รายการ")
print(f"📦 ทั้งหมด: {products.count()} รายการ")
print("=" * 70)

# แสดง URL ตัวอย่าง
print("\n📋 ตัวอย่าง URL ที่อัปเดตแล้ว:")
updated_products = Product.objects.exclude(image='')[:3]
for p in updated_products:
    print(f"   • Product {p.id}: {p.image}")
print("=" * 70)