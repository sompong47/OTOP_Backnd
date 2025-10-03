import os
import django
import cloudinary
import cloudinary.uploader
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otop_project.settings')
django.setup()

# -----------------------------
# ตั้งค่า Cloudinary ตรงนี้เลย
# -----------------------------
cloudinary.config(
    cloud_name='dam4zvtx7',
    api_key='969522454121228',
    api_secret='hm-5g8nJmZyfzX20Sua8P-ojNiM',
)

from otop_app.models import Product

print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
if not os.path.exists(settings.MEDIA_ROOT):
    print("❌ Media folder ไม่พบ")
    exit(1)

products = Product.objects.all()
for p in products:
    try:
        if not p.image or p.image.name.startswith('http'):
            print(f"⏭ Product {p.id} - ไม่มีรูปหรือเป็น URL แล้ว")
            continue

        file_path = os.path.join(settings.MEDIA_ROOT, p.image.name)
        if not os.path.exists(file_path):
            print(f"❌ Product {p.id} - ไฟล์ไม่พบ: {file_path}")
            continue

        result = cloudinary.uploader.upload(file_path, folder="products")
        secure_url = result.get('secure_url')
        if not secure_url:
            print(f"❌ Product {p.id} - อัปโหลดไม่สำเร็จ")
            continue

        p.image = secure_url
        p.save()
        print(f"✅ Product {p.id} - อัปเดตเรียบร้อย: {secure_url}")

    except Exception as e:
        print(f"❌ Product {p.id} - อัปโหลดล้มเหลว: {str(e)}")
