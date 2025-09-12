from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from otop_app.models import Category, Seller, Product

class Command(BaseCommand):
    help = 'Load sample OTOP data'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'name': 'เกษตรผลิตภัณฑ์', 'description': 'ผลิตภัณฑ์จากเกษตรกร'},
            {'name': 'หัตถกรรม', 'description': 'งานฝีมือพื้นบ้าน'},
            {'name': 'อาหารแปรรูป', 'description': 'อาหารแปรรูปจากธรรมชาติ'},
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(**cat_data)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create users and sellers
        sellers_data = [
            {'username': 'seller1', 'name': 'วิไลเกษตรกร', 'phone': '081-234-5678'},
            {'username': 'seller2', 'name': 'สหกรณ์เกษตรกรศรีสะเกษ', 'phone': '081-345-6789'},
            {'username': 'seller3', 'name': 'กลุ่มทอผ้าบ้านโคกตาล', 'phone': '081-456-7890'},
        ]

        for seller_data in sellers_data:
            user, created = User.objects.get_or_create(
                username=seller_data['username'],
                defaults={'email': f"{seller_data['username']}@example.com"}
            )
            
            seller, created = Seller.objects.get_or_create(
                user=user,
                defaults={
                    'name': seller_data['name'],
                    'phone': seller_data['phone'],
                    'address': 'ศรีสะเกษ',
                    'is_verified': True
                }
            )
            if created:
                self.stdout.write(f'Created seller: {seller.name}')

        # Create products
        products_data = [
            {
                'name': 'หอมแดงศรีสะเกษ',
                'description': 'หอมแดงคุณภาพดีจากเกษตรกรท้องถิน รสหวานกรอบ',
                'price': 45.00,
                'category': 'เกษตรผลิตภัณฑ์',
                'seller': 'วิไลเกษตรกร',
                'stock': 50
            },
            {
                'name': 'กระเทียมไทย',
                'description': 'กระเทียมสดใหม่ หอมเข้มข้น จากแปลงเกษตรอินทรีย์',
                'price': 80.00,
                'category': 'เกษตรผลิตภัณฑ์',
                'seller': 'สหกรณ์เกษตรกรศรีสะเกษ',
                'stock': 30
            },
            {
                'name': 'ผ้าไหมไทยแท้',
                'description': 'ผ้าไหมทอมือลายดั้งเดิม สีสวยงาม คุณภาพเยี่ยม',
                'price': 1200.00,
                'category': 'หัตถกรรม',
                'seller': 'กลุ่มทอผ้าบ้านโคกตาล',
                'stock': 15
            }
        ]

        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            seller = Seller.objects.get(name=prod_data['seller'])
            
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'category': category,
                    'seller': seller,
                    'stock': prod_data['stock'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample OTOP data!')
        )