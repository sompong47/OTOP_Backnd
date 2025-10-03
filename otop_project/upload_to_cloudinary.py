import os
import django
import cloudinary.uploader
from django.conf import settings

# ตั้งค่า Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otop_project.settings')
django.setup()

from otop_app.models import Product

# -----------------------------
# ตรวจสอบว่า Media Root มีอยู่
print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
if not os.path.exists(settings.MEDIA_ROOT):
    print("❌ Media folder ไม่พบ")
    exit(1)

# -----------------------------
# อัปโหลดรูปเก่าทั้งหมด
products = Product.objects.all()
for p in products:
    try:
        # ตรวจสอบว่ามีรูป
        if not p.image or p.image.name.startswith('http'):
            print(f"⏭ Product {p.id} ไม่มีรูปหรือเป็น URL แล้ว")
            continue

        # path ของไฟล์เก่า
        file_path = os.path.join(settings.MEDIA_ROOT, p.image.name)
        if not os.path.exists(file_path):
            print(f"❌ Product {p.id} ไฟล์ไม่พบ: {file_path}")
            continue

        # อัปโหลดไป Cloudinary
        result = cloudinary.uploader.upload(file_path, folder="products")
        p.image = result['secure_url']  # อัปเดต URL ของ Cloudinary
        p.save()
        print(f"✅ Product {p.id} อัปเดตเรียบร้อย: {p.image}")

    except Exception as e:
        print(f"❌ Product {p.id} อัปโหลดล้มเหลว: {str(e)}")
