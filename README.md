# OTOP Backend API

REST API สำหรับระบบจัดการผลิตภัณฑ์ OTOP (One Tambon One Product) พัฒนาด้วย Django REST Framework

## 🚀 เทคโนโลジีที่ใช้

- **Django** - Web Framework
- **Django REST Framework** - สำหรับสร้าง REST API
- **Simple JWT** - สำหรับ Authentication
- **SQLite/PostgreSQL** - Database

## 📋 ความต้องการของระบบ

- Python 3.8+
- pip (Python package manager)
- Virtual Environment (แนะนำ)

## 🛠️ การติดตั้ง

### 1. Clone Repository

```bash
git clone https://github.com/sompong47/OTOP_Backnd.git
cd OTOP_Backnd
```

### 2. สร้าง Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. สร้าง Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 6. รันเซิร์ฟเวอร์

```bash
python manage.py runserver
```

เซิร์ฟเวอร์จะรันที่ `http://127.0.0.1:8000/`

---

## 📚 API Documentation

### Base URL

**Local Development:**
```
http://127.0.0.1:8000/api/
```

**Production (Railway):**
```
https://otopbacknd-production.up.railway.app/api/
```

---

## 🔐 Authentication APIs

### 1. ลงทะเบียนผู้ใช้ใหม่

**Endpoint:** `POST /api/register/`

**Request Body:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securePassword123",
  "password2": "securePassword123",
  "first_name": "Test",
  "last_name": "User"
}
```

**Response:**
```json
{
  "success": true,
  "message": "สมัครสมาชิกสำเร็จ",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

**วิธีทดสอบ:**
```bash
# Local
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securePassword123",
    "password2": "securePassword123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Production
curl -X POST https://otopbacknd-production.up.railway.app/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securePassword123",
    "password2": "securePassword123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

---

### 2. เข้าสู่ระบบ (Get Token)

**Endpoint:** `POST /api/token/`

**Request Body:**
```json
{
  "username": "testuser",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**วิธีทดสอบ:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securePassword123"
  }'
```

---

### 3. Refresh Token

**Endpoint:** `POST /api/token/refresh/`

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 4. ดูโปรไฟล์ผู้ใช้

**Endpoint:** `GET /api/profile/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User"
}
```

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🛍️ Product APIs

### 1. ดูรายการสินค้าทั้งหมด

**Endpoint:** `GET /api/products/`

**Query Parameters:**
- `search` - ค้นหาตามชื่อ, คำอธิบาย, หมวดหมู่
- `ordering` - เรียงลำดับ (price, -price, created_at, -created_at)

**Response:**
```json
[
  {
    "id": 1,
    "name": "ผ้าไหมไทย",
    "description": "ผ้าไหมทอมือจากบ้านหนองหาน",
    "price": "1500.00",
    "stock": 20,
    "image": "/media/products/silk.jpg",
    "category": {
      "id": 1,
      "name": "ผ้าทอ"
    },
    "seller": {
      "id": 1,
      "shop_name": "ร้านผ้าไหมอุบล"
    },
    "is_active": true,
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

**วิธีทดสอบ:**
```bash
# ดูสินค้าทั้งหมด
curl -X GET http://127.0.0.1:8000/api/products/

# ค้นหาสินค้า
curl -X GET "http://127.0.0.1:8000/api/products/?search=ผ้าไหม"

# เรียงลำดับตามราคา
curl -X GET "http://127.0.0.1:8000/api/products/?ordering=price"
```

---

### 2. ดูรายละเอียดสินค้า

**Endpoint:** `GET /api/products/{id}/`

**Response:**
```json
{
  "id": 1,
  "name": "ผ้าไหมไทย",
  "description": "ผ้าไหมทอมือจากบ้านหนองหาน คุณภาพเยี่ยม",
  "price": "1500.00",
  "stock": 20,
  "image": "/media/products/silk.jpg",
  "category": {
    "id": 1,
    "name": "ผ้าทอ"
  },
  "seller": {
    "id": 1,
    "shop_name": "ร้านผ้าไหมอุบล",
    "phone": "081-234-5678"
  },
  "average_rating": 4.5,
  "review_count": 12,
  "is_active": true,
  "created_at": "2025-01-15T10:30:00Z"
}
```

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/products/1/
```

---

### 3. เพิ่มรีวิวสินค้า

**Endpoint:** `POST /api/products/{product_id}/reviews/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "rating": 5,
  "comment": "สินค้าดีมาก คุณภาพเยี่ยม"
}
```

**Response:**
```json
{
  "success": true,
  "message": "เพิ่มรีวิวสำเร็จ",
  "review": {
    "id": 1,
    "user": "testuser",
    "rating": 5,
    "comment": "สินค้าดีมาก คุณภาพเยี่ยม",
    "created_at": "2025-01-15T11:00:00Z"
  }
}
```

**วิธีทดสอบ:**
```bash
curl -X POST http://127.0.0.1:8000/api/products/1/reviews/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "สินค้าดีมาก คุณภาพเยี่ยม"
  }'
```

---

### 4. ดูรีวิวสินค้า

**Endpoint:** `GET /api/products/{product_id}/reviews/`

**Response:**
```json
[
  {
    "id": 1,
    "user": "testuser",
    "rating": 5,
    "comment": "สินค้าดีมาก คุณภาพเยี่ยม",
    "created_at": "2025-01-15T11:00:00Z"
  }
]
```

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/products/1/reviews/
```

---

## 📦 Category APIs

### 1. ดูหมวดหมู่ทั้งหมด

**Endpoint:** `GET /api/categories/`

**Response:**
```json
[
  {
    "id": 1,
    "name": "ผ้าทอ",
    "description": "ผ้าทอพื้นเมือง",
    "image": "/media/categories/fabric.jpg"
  },
  {
    "id": 2,
    "name": "อาหารแปรรูป",
    "description": "ผลิตภัณฑ์อาหารแปรรูป"
  }
]
```

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/categories/
```

---

### 2. ดูรายละเอียดหมวดหมู่

**Endpoint:** `GET /api/categories/{id}/`

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/categories/1/
```

---

## 🛒 Order APIs

### 1. สร้างคำสั่งซื้อ

**Endpoint:** `POST /api/orders/create/`

**Request Body:**
```json
{
  "customer_name": "สมชาย ใจดี",
  "customer_email": "somchai@example.com",
  "customer_phone": "081-234-5678",
  "shipping_address": "123 ถ.หลวง ต.ในเมือง อ.เมือง จ.อุบลราชธานี 34000",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": "1500.00"
    },
    {
      "product_id": 2,
      "quantity": 1,
      "price": "500.00"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "สั่งซื้อสำเร็จ",
  "data": {
    "id": 1,
    "order_number": "ORD-2025-0001",
    "customer_name": "สมชาย ใจดี",
    "customer_email": "somchai@example.com",
    "total_amount": "3500.00",
    "status": "pending",
    "created_at": "2025-01-15T12:00:00Z",
    "items": [
      {
        "product": {
          "id": 1,
          "name": "ผ้าไหมไทย"
        },
        "quantity": 2,
        "price": "1500.00",
        "subtotal": "3000.00"
      }
    ]
  }
}
```

**วิธีทดสอบ:**
```bash
curl -X POST http://127.0.0.1:8000/api/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "สมชาย ใจดี",
    "customer_email": "somchai@example.com",
    "customer_phone": "081-234-5678",
    "shipping_address": "123 ถ.หลวง ต.ในเมือง อ.เมือง จ.อุบลราชธานี 34000",
    "items": [
      {
        "product_id": 1,
        "quantity": 2,
        "price": "1500.00"
      }
    ]
  }'
```

---

### 2. ดูคำสั่งซื้อของฉัน

**Endpoint:** `GET /api/my-orders/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "order_number": "ORD-2025-0001",
    "customer_name": "สมชาย ใจดี",
    "total_amount": "3500.00",
    "status": "pending",
    "created_at": "2025-01-15T12:00:00Z",
    "items": [
      {
        "product": {
          "id": 1,
          "name": "ผ้าไหมไทย"
        },
        "quantity": 2,
        "price": "1500.00"
      }
    ]
  }
]
```

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/my-orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 3. ดูรายละเอียดคำสั่งซื้อ

**Endpoint:** `GET /api/orders/{id}/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/orders/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 4. อัพเดทสถานะคำสั่งซื้อ (สำหรับผู้ขาย)

**Endpoint:** `PATCH /api/orders/{id}/status/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "status": "processing"
}
```

**สถานะที่ใช้ได้:**
- `pending` - รอดำเนินการ
- `processing` - กำลังเตรียมสินค้า
- `shipped` - จัดส่งแล้ว
- `delivered` - ส่งถึงแล้ว
- `cancelled` - ยกเลิก

**Response:**
```json
{
  "success": true,
  "message": "อัพเดทสถานะสำเร็จ",
  "status": "processing"
}
```

**วิธีทดสอบ:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/orders/1/status/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "processing"
  }'
```

---

## 👨‍💼 Seller APIs

### 1. ดูข้อมูลร้านค้า

**Endpoint:** `GET /api/seller/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "shop_name": "ร้านผ้าไหมอุบล",
  "description": "จำหน่ายผ้าไหมทอมือคุณภาพสูง",
  "phone": "081-234-5678",
  "address": "123 ถ.หลวง ต.ในเมือง อ.เมือง จ.อุบลราชธานี"
}
```

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/seller/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 2. ดู Dashboard ผู้ขาย

**Endpoint:** `GET /api/seller/dashboard/`

**Response:**
```json
{
  "success": true,
  "data": {
    "today_sales": 1500.0,
    "sales_growth": 5.2,
    "new_orders": 12,
    "pending_orders": 3,
    "total_products": 25,
    "low_stock_products": 2,
    "average_rating": 4.5,
    "total_reviews": 48,
    "recent_activities": [
      {
        "type": "order",
        "title": "คำสั่งซื้อใหม่",
        "subtitle": "มีคำสั่งซื้อใหม่ 3 รายการ",
        "time": "5 นาทีที่แล้ว"
      }
    ]
  }
}
```

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/seller/dashboard/
```

---

### 3. ดูสินค้าของร้าน

**Endpoint:** `GET /api/seller/products/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "ผ้าไหมไทย",
    "price": "1500.00",
    "stock": 20,
    "is_active": true,
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/seller/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 4. เพิ่มสินค้าใหม่

**Endpoint:** `POST /api/seller/products/`

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
name: ผ้าไหมลายดอก
description: ผ้าไหมทอมือลายดอกไม้
price: 1800.00
stock: 15
category: 1
image: [file]
```

**วิธีทดสอบ:**
```bash
curl -X POST http://127.0.0.1:8000/api/seller/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "name=ผ้าไหมลายดอก" \
  -F "description=ผ้าไหมทอมือลายดอกไม้" \
  -F "price=1800.00" \
  -F "stock=15" \
  -F "category=1" \
  -F "image=@/path/to/image.jpg"
```

---

### 5. แก้ไขสินค้า

**Endpoint:** `PUT/PATCH /api/seller/products/{id}/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "ผ้าไหมไทย (ปรับราคา)",
  "price": "1400.00",
  "stock": 25
}
```

**วิธีทดสอบ:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/seller/products/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price": "1400.00",
    "stock": 25
  }'
```

---

### 6. ลบสินค้า

**Endpoint:** `DELETE /api/seller/products/{id}/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**วิธีทดสอบ:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/seller/products/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 7. ดูคำสั่งซื้อของร้าน

**Endpoint:** `GET /api/seller/orders/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": 1,
    "order_number": "ORD-2025-0001",
    "customer_name": "สมชาย ใจดี",
    "total_amount": "3500.00",
    "status": "pending",
    "created_at": "2025-01-15T12:00:00Z"
  }
]
```

**วิธีทดสอบ:**
```bash
curl -X GET http://127.0.0.1:8000/api/seller/orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🧪 การทดสอบด้วย Postman

### ขั้นตอนการทดสอบ:

1. **ดาวน์โหลด Postman**: https://www.postman.com/downloads/

2. **สร้าง Collection ใหม่**:
   - เปิด Postman
   - คลิก "New" → "Collection"
   - ตั้งชื่อ "OTOP API"

3. **ตั้งค่า Environment Variables**:
   - คลิก "Environments"
   - สร้าง Environment ใหม่ชื่อ "OTOP Local"
   - เพิ่มตัวแปร:
     ```
     base_url: http://127.0.0.1:8000/api
     production_url: https://otopbacknd-production.up.railway.app/api
     access_token: (จะได้หลังจาก login)
     ```

4. **ทดสอบ APIs ตามลำดับ**:

   **เลือก Environment**: OTOP Local (สำหรับ local) หรือใช้ production_url

   **Step 1: ลงทะเบียน**
   ```
   POST {{base_url}}/register/
   # หรือ POST {{production_url}}/register/
   Body (JSON):
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "testpass123",
     "password2": "testpass123",
     "first_name": "Test",
     "last_name": "User"
   }
   ```

   **Step 2: Login**
   ```
   POST {{base_url}}/token/
   # หรือ POST {{production_url}}/token/
   Body (JSON):
   {
     "username": "testuser",
     "password": "testpass123"
   }
   ```
   - คัดลอก `access` token จาก response
   - เพิ่มใน Environment Variables: `access_token`

   **Step 3: ดูโปรไฟล์**
   ```
   GET {{base_url}}/profile/
   Headers:
   Authorization: Bearer {{access_token}}
   ```

   **Step 4: ดูสินค้าทั้งหมด**
   ```
   GET {{base_url}}/products/
   ```

   **Step 5: สร้างคำสั่งซื้อ**
   ```
   POST {{base_url}}/orders/create/
   Body (JSON):
   {
     "customer_name": "Test User",
     "customer_email": "test@example.com",
     "customer_phone": "0812345678",
     "shipping_address": "123 Test St.",
     "items": [
       {
         "product_id": 1,
         "quantity": 2,
         "price": "1500.00"
       }
     ]
   }
   ```

---

## 🔍 Error Codes

| Status Code | Description |
|------------|-------------|
| 200 | OK - สำเร็จ |
| 201 | Created - สร้างข้อมูลสำเร็จ |
| 400 | Bad Request - ข้อมูลไม่ถูกต้อง |
| 401 | Unauthorized - ไม่มีสิทธิ์เข้าถึง (ไม่ได้ login) |
| 403 | Forbidden - ไม่มีสิทธิ์ดำเนินการ |
| 404 | Not Found - ไม่พบข้อมูล |
| 500 | Internal Server Error - เกิดข้อผิดพลาดในระบบ |

---

## 📝 Response Format

### Success Response
```json
{
  "success": true,
  "message": "ดำเนินการสำเร็จ",
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "message": "ข้อความแสดงข้อผิดพลาด",
  "errors": {
    "field": ["error message"]
  }
}
```

---

## 🔒 Authorization

APIs ส่วนใหญ่ต้องการ JWT Token ในการเข้าถึง:

```
Authorization: Bearer {access_token}
```

### Token Expiration
- **Access Token**: หมดอายุใน 60 นาที
- **Refresh Token**: หมดอายุใน 7 วัน

---

## 🗄️ Database Models

### User
- username
- email
- password
- first_name
- last_name

### Product
- name
- description
- price
- stock
- image
- category (FK)
- seller (FK)
- is_active
- created_at

### Order
- order_number
- customer_name
- customer_email
- customer_phone
- shipping_address
- total_amount
- status
- created_at

### OrderItem
- order (FK)
- product (FK)
- quantity
- price

### Category
- name
- description
- image

### Seller
- user (OneToOne)
- shop_name
- description
- phone
- address

### ProductReview
- user (FK)
- product (FK)
- rating
- comment
- created_at

---

## 🚀 Deployment

โปรเจคนี้ได้ถูก Deploy บน **Railway** แล้ว

### 🌐 Production URL
```
https://otopbacknd-production.up.railway.app/
```

### ขั้นตอนการ Deploy บน Railway:

#### 1. สร้างบัญชี Railway
- เข้าไปที่ https://railway.app/
- Sign up ด้วย GitHub Account

#### 2. เชื่อมต่อ GitHub Repository
- คลิก "New Project"
- เลือก "Deploy from GitHub repo"
- เลือก repository `OTOP_Backnd`

#### 3. ตั้งค่า Environment Variables
ไปที่ Variables tab และเพิ่ม:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=otopbacknd-production.up.railway.app
DATABASE_URL=postgresql://... (Railway จะสร้างให้อัตโนมัติ)
```

#### 4. เพิ่ม PostgreSQL Database
- ใน Project คลิก "New"
- เลือก "Database" → "PostgreSQL"
- Railway จะสร้าง Database และตั้งค่า DATABASE_URL ให้อัตโนมัติ

#### 5. สร้างไฟล์ที่จำเป็น

**Procfile** (สำหรับบอก Railway ว่าจะรันอย่างไร):
```
web: gunicorn config.wsgi --log-file -
release: python manage.py migrate
```

**runtime.txt** (ระบุเวอร์ชัน Python):
```
python-3.11.0
```

**requirements.txt** (ต้องมี):
```
Django>=4.2
djangorestframework
django-cors-headers
djangorestframework-simplejwt
Pillow
gunicorn
psycopg2-binary
whitenoise
```

#### 6. ตั้งค่า Django สำหรับ Production

**settings.py**:
```python
import os
import dj_database_url

# SECURITY
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Database
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }

# Static files (whitenoise)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # เพิ่มบรรทัดนี้
    # ... middleware อื่นๆ
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### 7. Deploy
- Push โค้ดไปที่ GitHub
- Railway จะ auto-deploy ทุกครั้งที่มีการ push
- รอ build และ deploy เสร็จ (ประมาณ 2-5 นาที)

#### 8. Run Migrations
Railway จะรัน migrations อัตโนมัติจาก Procfile หรือรันเองได้:
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

### เช็คสถานะ Deployment
```bash
# ดู logs
railway logs

# เข้า shell
railway run python manage.py shell
```

### 💡 Tips สำหรับ Railway:
- ✅ ฟรี 500 ชั่วโมง/เดือน หรือ $5 credit
- ✅ Auto-deploy เมื่อ push to GitHub
- ✅ ให้ PostgreSQL database ฟรี
- ✅ มี SSL certificate อัตโนมัติ
- ✅ Environment variables ที่ปลอดภัย

---

### Alternative Deployment Options:

**Render** (ฟรี):
```
https://render.com/
```

**Heroku** (มีค่าใช้จ่าย):
```
https://www.heroku.com/
```

**DigitalOcean App Platform**:
```
https://www.digitalocean.com/products/app-platform
```

---

### สำหรับ Production:

1. **ตั้งค่า Environment Variables**
```bash
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
```

2. **Collect Static Files**
```bash
python manage.py collectstatic
```

3. **ใช้ Gunicorn**
```bash
pip install gunicorn
gunicorn config.wsgi:application
```

---

## 📞 ติดต่อ

- **Developer**: Sompong
- **GitHub**: [@sompong47](https://github.com/sompong47)
- **Repository**: [OTOP_Backnd](https://github.com/sompong47/OTOP_Backnd)

---

## 📄 License

โปรเจคนี้เป็นส่วนหนึ่งของการศึกษา

---

⭐ **Happy Coding!** ถ้าชอบโปรเจคนี้ อย่าลืมกด Star ให้ด้วยนะครับ!
