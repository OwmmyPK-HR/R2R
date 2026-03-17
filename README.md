# R2R System - ระบบขอรับการสนับสนุนการตีพิมพ์บทความวิจัย

## เกี่ยวกับโปรเจค
ระบบแบบฟอร์มออนไลน์สำหรับการขอรับการสนับสนุนการตีพิมพ์บทความวิจัย สำหรับมหาวิทยาลัยเทคโนโลยีราชมงคลธัญบุรี

## คุณสมบัติ
- ✅ ฟอร์มการกรอกข้อมูลแบบออนไลน์
- ✅ ระบบอัปโหลดไฟล์เอกสารประกอบ (PDF, รูปภาพ)
- ✅ การคำนวณเงินสนับสนุนอัตโนมัติ
- ✅ ระบบจัดการข้อมูลสำหรับผู้ดูแล (Admin)
- ✅ การสร้าง PDF รายงานอัตโนมัติ
- ✅ การตั้งค่าระบบ (Admin Settings)
- ✅ ระบบ CSRF Protection
- ✅ ระบบ Rate Limiting
- ✅ ระบบบันทึกการทำงาน (System Logging)
- ✅ ระบบจัดการ Token (Token Management)
- ✅ REST API สำหรับ Logs และ Tokens
- ✅ รองรับ Reverse Proxy / HTTPS (ProxyFix)
- ✅ Database Migration Tool

## เทคโนโลยีที่ใช้
- **Backend**: Flask (Python 3.11.9)
- **Database**: SQLite (Local) / PostgreSQL (Production)
- **Frontend**: HTML, CSS, JavaScript
- **PDF Generation**: fpdf2
- **Server**: Gunicorn
- **Security**: Flask-WTF (CSRF), Flask-Limiter (Rate Limiting), Werkzeug

## การติดตั้งและใช้งาน

### ติดตั้งในเครื่อง Local
1. Clone repository นี้
```bash
git clone https://github.com/OwmmyPK-HR/R2R.git
cd R2R
```

2. สร้าง Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# หรือ source venv/bin/activate  # Mac/Linux
```

3. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

4. ตั้งค่า Environment Variables โดยคัดลอกไฟล์ตัวอย่าง
```bash
copy .env.example .env   # Windows
# หรือ cp .env.example .env  # Mac/Linux
```
แก้ไขไฟล์ `.env` ตามที่ต้องการ

5. รันแอป
```bash
python app.py
```

6. เปิดเว็บไซต์ที่ `http://127.0.0.1:5000`

### Migration ฐานข้อมูล (กรณีอัพเดทจาก Version เก่า)
หากมีฐานข้อมูลเดิมและต้องการเพิ่มฟิลด์ใหม่ ให้รันสคริปต์:
```bash
python migrate_database.py
```

### Deploy บน Heroku
1. สร้าง Heroku App
```bash
heroku create your-app-name
```

2. ตั้งค่า Environment Variables
```bash
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set ADMIN_PASSWORD=your-admin-password
heroku config:set FLASK_ENV=production
heroku config:set APP_ENV=production
heroku config:set SESSION_LIFETIME_MINUTES=480
heroku config:set LIMITER_STORAGE_URI=memory://
heroku config:set WEB_CONCURRENCY=1
```

3. Push โค้ดขึ้น Heroku
```bash
git push heroku main
```

### Deploy บน Railway
1. เชื่อมต่อ GitHub repository กับ Railway
2. ตั้งค่า Environment Variables:
   - `SECRET_KEY`: รหัสลับสำหรับ Flask
   - `ADMIN_PASSWORD`: รหัสผ่าน Admin
   - `FLASK_ENV`: `production`
   - `APP_ENV`: `production`
   - `SESSION_LIFETIME_MINUTES`: `480`
   - `LIMITER_STORAGE_URI`: `memory://`
   - `WEB_CONCURRENCY`: `1`
3. Deploy อัตโนมัติ

## การตั้งค่า Environment Variables

ดูไฟล์ `.env.example` สำหรับการตั้งค่า Local Development และ `.env.production.example` สำหรับ Production

### ไฟล์ .env (สำหรับ Local Development)
คัดลอกจาก `.env.example` แล้วแก้ไขค่าตามต้องการ:

```bash
# Flask Configuration
SECRET_KEY=replace-with-a-random-64-char-hex-secret
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_HOST=127.0.0.1
PORT=5000

# Database Configuration
DATABASE_URL=sqlite:///database.db

# Admin Configuration
ADMIN_PASSWORD=replace-with-a-strong-admin-password

# Application Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
```

### ไฟล์ .env (สำหรับ Production)
คัดลอกจาก `.env.production.example` แล้วแก้ไขค่าตามต้องการ:

```bash
# Flask core
SECRET_KEY=replace-with-a-random-64-char-hex-secret
FLASK_ENV=production
FLASK_DEBUG=0
APP_ENV=production
FLASK_HOST=0.0.0.0
PORT=8000

# Reverse proxy / HTTPS
USE_PROXY_FIX=1
PREFERRED_URL_SCHEME=https
SESSION_COOKIE_SECURE=1
SESSION_COOKIE_HTTPONLY=1
SESSION_COOKIE_SAMESITE=Lax

# Database Configuration (PostgreSQL for Production)
DATABASE_URL=postgresql://username:password@hostname:5432/database_name

# Admin Configuration
ADMIN_PASSWORD=change-this-admin-password

# Application Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
SESSION_LIFETIME_MINUTES=480

# Rate limiter
LIMITER_STORAGE_URI=memory://
WEB_CONCURRENCY=1
```

### คำอธิบาย Environment Variables

#### Flask Configuration
- **SECRET_KEY**: คีย์ลับสำหรับการเข้ารหัส session และ cookies
  - **วิธีสร้าง**: ใช้คำสั่ง `python -c "import secrets; print(secrets.token_hex(32))"`
  - ⚠️ **สำคัญ**: ต้องเปลี่ยนเป็นค่าใหม่ทุกครั้งในการใช้งาน Production และห้ามละเว้นสำหรับ Production (ระบบจะ error หากไม่ตั้งค่า)
- **FLASK_ENV** / **APP_ENV**: สภาพแวดล้อมการทำงาน (`production` หรือ `development`)
- **FLASK_DEBUG**: เปิด/ปิด Debug Mode (`0` = ปิด, `1` = เปิด) - ต้องปิดใน Production
- **FLASK_HOST**: IP ที่รับการเชื่อมต่อ (`127.0.0.1` สำหรับ local, `0.0.0.0` สำหรับ server)
- **PORT**: พอร์ตที่ใช้รัน (`5000` สำหรับ development, `8000` สำหรับ production)

#### Database Configuration
- **DATABASE_URL**: URL สำหรับเชื่อมต่อฐานข้อมูล
  - **PostgreSQL**: `postgresql://username:password@hostname:5432/database_name`
  - **SQLite** (สำหรับ development เท่านั้น): `sqlite:///database.db`
  - **Heroku PostgreSQL**: Heroku จะตั้งค่า `DATABASE_URL` ให้อัตโนมัติ

#### Admin Configuration
- **ADMIN_PASSWORD**: รหัสผ่านตั้งต้นของผู้ดูแลระบบ
   - ⚠️ **สำคัญ**: ใน production ต้องตั้งค่า และห้ามใช้ค่า default
   - ⚠️ **ข้อกำหนด**: ควรมีอย่างน้อย 12 ตัวอักษร
   - หมายเหตุ: หลังระบบบันทึกรหัสผ่านแบบ hash ลงฐานข้อมูลแล้ว การเปลี่ยนค่าใน `.env` อย่างเดียวจะไม่เปลี่ยนรหัสผ่านที่ใช้งานอยู่ทันที

#### Reverse Proxy / HTTPS (สำหรับ Production)
- **USE_PROXY_FIX**: เปิดใช้งาน ProxyFix middleware (`1` = เปิด) เมื่อมี reverse proxy อยู่หน้าระบบ
- **PREFERRED_URL_SCHEME**: โปรโตคอลที่ใช้ (`https` สำหรับ production)
- **SESSION_COOKIE_SECURE**: ส่ง cookie เฉพาะผ่าน HTTPS (`1` = เปิด)
- **SESSION_COOKIE_HTTPONLY**: ป้องกัน JavaScript เข้าถึง cookie (`1` = เปิด)
- **SESSION_COOKIE_SAMESITE**: ควบคุม cross-site cookie (`Lax` หรือ `Strict`)

#### Application Settings
- **MAX_CONTENT_LENGTH**: ขนาดไฟล์สูงสุดที่อนุญาต (bytes) - ค่า default = 16MB
- **UPLOAD_FOLDER**: โฟลเดอร์สำหรับเก็บไฟล์ที่อัปโหลด
- **SESSION_LIFETIME_MINUTES**: อายุ session ของ admin (default 480 นาที)
- **LIMITER_STORAGE_URI**: backend storage ของ rate limiter (`memory://` หรือ `redis://...`)
- **WEB_CONCURRENCY**: จำนวน Gunicorn workers (`1` เมื่อใช้ `memory://`)

### ⚠️ ข้อควรระวัง
1. **อย่า commit ไฟล์ .env ลงใน Git**
   - เพิ่มบรรทัด `.env` และ `*.env` ใน `.gitignore`
   
2. **สำหรับ Heroku/Railway**
   - ไม่ต้องใช้ไฟล์ `.env`
   - ตั้งค่าผ่าน Dashboard (Config Vars) แทน

3. **สำหรับ Production Server**
   - ใช้ไฟล์ `.env` หรือตั้งค่า environment variables ในระบบโดยตรง
   - ตรวจสอบให้แน่ใจว่าไฟล์ `.env` มีสิทธิ์การอ่านที่เหมาะสม (chmod 600)

### การใช้งานไฟล์ .env ในเครื่อง Local
แอปจะโหลดไฟล์ `.env` จากโฟลเดอร์ root ของโปรเจกต์ให้อัตโนมัติเมื่อมีการติดตั้ง dependencies จาก `requirements.txt`

### การใช้งานไฟล์สำหรับ Production
- ใช้ `.env.production.example` เป็นแม่แบบสำหรับ production
- ถ้า deploy บน VPS ที่คุณดูแลเอง ให้คัดลอกค่าที่จำเป็นไปใส่ `.env` บนเซิร์ฟเวอร์หรือ export เป็น system environment variables
- ถ้า deploy บน Heroku, Railway, Render ให้ใช้ค่าจาก `.env.production.example` ไปตั้งใน Dashboard แทนการอัปโหลดไฟล์

## การใช้งาน

### สำหรับผู้ใช้ทั่วไป
1. เข้าสู่เว็บไซต์
2. กรอกข้อมูลในแบบฟอร์ม
3. อัปโหลดเอกสารประกอบ (PDF หรือรูปภาพสำหรับบางช่อง)
4. ส่งแบบฟอร์ม

### สำหรับผู้ดูแลระบบ (Admin)
- รหัสผ่าน Admin: ใช้ค่าจาก `ADMIN_PASSWORD` ใน environment
- สำหรับ production ระบบจะไม่เริ่มทำงานหากไม่ได้ตั้ง `ADMIN_PASSWORD` หรือใช้ค่าที่ไม่ปลอดภัย
- คลิก "Admin Login" เพื่อเข้าสู่ระบบจัดการ
- ดูข้อมูลที่ส่งเข้ามา
- ดาวน์โหลด PDF รายงาน
- ตั้งค่าระบบที่ `/admin/settings`

## API Endpoints (Admin Only)

| Endpoint | Method | คำอธิบาย |
|----------|--------|---------|
| `/api/logs` | GET | ดึงรายการ System Logs |
| `/api/logs/submission/<id>` | GET | ดึง Logs ของคำขอที่ระบุ |
| `/api/tokens` | GET | ดึงรายการ API Tokens |
| `/api/tokens/<id>` | DELETE | ลบ Token |
| `/api/tokens/cleanup` | POST | ลบ Tokens ที่หมดอายุแล้ว |

หมายเหตุความปลอดภัย:
- ทุก endpoint ต้องมี admin session (`admin_logged_in`)
- endpoint ที่เปลี่ยนข้อมูล (`DELETE`, `POST`) ต้องส่ง CSRF token
- มี rate limit ตาม route ใน `app.py`

> ดูรายละเอียดการใช้งาน API เพิ่มเติมในไฟล์ `LOGGING_AND_TOKENS_GUIDE.md`

## โครงสร้างโปรเจค
```
R2R-System/
├── app.py                       # Main Flask application
├── wsgi.py                      # WSGI entry point
├── logging_utils.py             # ระบบบันทึกการทำงาน (System Logging)
├── token_manager.py             # ระบบจัดการ Token
├── migrate_database.py          # สคริปต์ Migration ฐานข้อมูล
├── test_logs_and_tokens.py      # ชุดทดสอบ Logging และ Token
├── requirements.txt             # Python dependencies
├── Procfile                     # Process config (release + web)
├── runtime.txt                  # Python version (3.11.9)
├── .env.example                 # ตัวอย่าง .env สำหรับ Local Development
├── .env.production.example      # ตัวอย่าง .env สำหรับ Production
├── DEPLOYMENT_GUIDE.md          # คู่มือการ Deploy
├── LOGGING_AND_TOKENS_GUIDE.md  # คู่มือระบบ Logging และ Token
├── LOGGING_AND_TOKENS_SETUP.md  # คู่มือตั้งค่าระบบ Logging และ Token
├── db/                          # สคริปต์จัดการฐานข้อมูล
│   ├── init_db.py               # สคริปต์สร้างฐานข้อมูลเริ่มต้น
│   ├── schema.sql               # Schema สำหรับ SQLite
│   ├── schema_postgres.sql      # Schema สำหรับ PostgreSQL
│   └── README.md                # คู่มือการจัดการฐานข้อมูล
├── static/                      # CSS, JS, fonts
├── templates/                   # HTML templates
│   ├── index.html               # ฟอร์มหลัก
│   ├── login.html               # หน้า Login
│   ├── admin.html               # หน้า Admin Dashboard
│   └── admin_settings.html      # หน้าตั้งค่า Admin
├── uploads/                     # ไฟล์ที่อัปโหลด
└── instance/                    # ฐานข้อมูล SQLite (local)
```

## ข้อมูลการติดต่อ
สำหรับคำถามหรือปัญหาการใช้งาน กรุณาติดต่อทีมพัฒนา

## เอกสารเพิ่มเติม
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - คู่มือการ Deploy แบบละเอียด
- [LOGGING_AND_TOKENS_GUIDE.md](LOGGING_AND_TOKENS_GUIDE.md) - คู่มือการใช้งานระบบ Logging และ Token
- [LOGGING_AND_TOKENS_SETUP.md](LOGGING_AND_TOKENS_SETUP.md) - คู่มือการตั้งค่าระบบ Logging และ Token
- [db/README.md](db/README.md) - คู่มือการจัดการฐานข้อมูล

---
© 2025 มหาวิทยาลัยเทคโนโลยีราชมงคลธัญบุรี
