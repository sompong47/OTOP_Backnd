"""
Django Management Command สำหรับอัปโหลดรูปไป Cloudinary
วางไฟล์นี้ที่: otop_app/management/commands/upload_to_cloudinary.py

รันด้วย: python manage.py upload_to_cloudinary
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from otop_app.models import Product
import cloudinary
import cloudinary.uploader


class Command(BaseCommand):
    help = 'อัปโหลดรูปสินค้าทั้งหมดไป Cloudinary'

    def handle(self, *args, **options):
        # ตั้งค่า Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )

        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("🚀 เริ่มอัปโหลดรูปภาพไป Cloudinary"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"☁️  Cloudinary: {settings.CLOUDINARY_CLOUD_NAME}")
        self.stdout.write("=" * 70)

        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(self.style.WARNING("⚠️  ไม่มีสินค้าในฐานข้อมูล"))
            return

        success_count = 0
        skip_count = 0
        error_count = 0
        no_image_count = 0

        for product in products:
            self.stdout.write(f"\n📦 Product {product.id}: {product.name}")
            
            if not product.image:
                self.stdout.write("   ℹ️  ไม่มีรูป - ข้าม")
                no_image_count += 1
                continue

            image_str = str(product.image)
            self.stdout.write(f"   📷 Image: {image_str}")

            # เช็คว่าเป็น Cloudinary URL หรือไม่
            if "cloudinary.com" in image_str or "res.cloudinary.com" in image_str:
                self.stdout.write(self.style.SUCCESS("   ✅ มี Cloudinary URL อยู่แล้ว"))
                skip_count += 1
                continue

            # อัปโหลดไป Cloudinary
            try:
                self.stdout.write("   ⬆️  กำลังอัปโหลด...")
                
                # ถ้าเป็น URL ให้อัปโหลดจาก URL
                if image_str.startswith(('http://', 'https://')):
                    result = cloudinary.uploader.upload(
                        image_str,
                        folder="otop_products",
                        public_id=f"product_{product.id}",
                        overwrite=True,
                        resource_type="image"
                    )
                else:
                    # ถ้าเป็น path local (ใช้ได้เฉพาะบน server ที่มีไฟล์)
                    import os
                    clean_path = image_str.replace("/media/", "").replace("media/", "")
                    local_path = os.path.join(settings.MEDIA_ROOT, clean_path)
                    
                    if not os.path.exists(local_path):
                        self.stdout.write(self.style.ERROR(f"   ❌ ไม่พบไฟล์: {local_path}"))
                        error_count += 1
                        continue
                    
                    result = cloudinary.uploader.upload(
                        local_path,
                        folder="otop_products",
                        public_id=f"product_{product.id}",
                        overwrite=True,
                        resource_type="image"
                    )
                
                secure_url = result['secure_url']
                product.image = secure_url
                product.save()
                
                self.stdout.write(self.style.SUCCESS(f"   ✅ สำเร็จ!"))
                self.stdout.write(f"   🔗 URL ใหม่: {secure_url}")
                success_count += 1
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ อัปโหลดล้มเหลว: {str(e)}"))
                error_count += 1

        # สรุปผลลัพธ์
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("📊 สรุปผลการอัปโหลด"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"✅ สำเร็จ: {success_count} รายการ")
        self.stdout.write(f"⏭️  ข้าม (มี Cloudinary URL): {skip_count} รายการ")
        self.stdout.write(f"ℹ️  ไม่มีรูป: {no_image_count} รายการ")
        self.stdout.write(f"❌ ล้มเหลว: {error_count} รายการ")
        self.stdout.write(f"📦 ทั้งหมด: {products.count()} รายการ")
        self.stdout.write("=" * 70)

        # แสดงตัวอย่าง URL
        self.stdout.write("\n📋 ตัวอย่าง URL ที่อัปเดตแล้ว:")
        updated_products = Product.objects.exclude(image='')[:3]
        for p in updated_products:
            self.stdout.write(f"   • Product {p.id}: {p.image}")
        self.stdout.write("=" * 70)