# R2R System - ระบบขอรับการสนับสนุนการตีพิมพ์บทความวิจัย

## เกี่ยวกับโปรเจค
ระบบแบบฟอร์มออนไลน์สำหรับการขอรับการสนับสนุนการตีพิมพ์บทความวิจัย สำหรับมหาวิทยาลัยเทคโนโลยีราชมงคลธัญบุรี

## คุณสมบัติ
- ✅ ฟอร์มการกรอกข้อมูลแบบออนไลน์
- ✅ ระบบอัปโหลดไฟล์เอกสารประกอบ
- ✅ การคำนวณเงินสนับสนุนอัตโนมัติ
- ✅ ระบบจัดการข้อมูลสำหรับผู้ดูแล (Admin)
- ✅ การสร้าง PDF รายงานอัตโนมัติ
- ✅ การตั้งค่าระบบ

## เทคโนโลยีที่ใช้
- **Backend**: Flask (Python)
- **Database**: SQLite (Local) / PostgreSQL (Production)
- **Frontend**: HTML, CSS, JavaScript
- **PDF Generation**: fpdf2
- **Server**: Gunicorn

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

4. รันแอป
```bash
python app.py
```

5. เปิดเว็บไซต์ที่ `http://127.0.0.1:5000`

### Deploy บน Heroku
1. สร้าง Heroku App
```bash
heroku create your-app-name
```

2. ตั้งค่า Environment Variables
```bash
heroku config:set SECRET_KEY=your-secret-key-here
```

3. Push โค้ดขึ้น Heroku
```bash
git push heroku main
```

### Deploy บน Railway
1. เชื่อมต่อ GitHub repository กับ Railway
2. ตั้งค่า Environment Variables:
   - `SECRET_KEY`: รหัสลับสำหรับ Flask
3. Deploy อัตโนมัติ

## การตั้งค่า Environment Variables




### ไฟล์ .env (สำหรับ Production)
สำหรับการ Deploy บน Server ของคุณเอง คุณต้องสร้างไฟล์ `.env` ในโฟลเดอร์ root ของโปรเจค

**ตัวอย่างไฟล์ .env:**
```bash
# Flask Configuration
SECRET_KEY=your-production-secret-key-here-please-change-this
FLASK_ENV=production
FLASK_DEBUG=0

# Database Configuration (PostgreSQL for Production)
DATABASE_URL=postgresql://username:password@hostname:5432/database_name

# Application Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
```

### คำอธิบาย Environment Variables

#### Flask Configuration
- **SECRET_KEY**: คีย์ลับสำหรับการเข้ารหัส session และ cookies
  - **วิธีสร้าง**: ใช้คำสั่ง `python -c "import secrets; print(secrets.token_hex(32))"`
  - ⚠️ **สำคัญ**: ต้องเปลี่ยนเป็นค่าใหม่ทุกครั้งในการใช้งาน Production
- **FLASK_ENV**: สภาพแวดล้อมการทำงาน (`production` หรือ `development`)
- **FLASK_DEBUG**: เปิด/ปิด Debug Mode (`0` = ปิด, `1` = เปิด) - ต้องปิดใน Production

#### Database Configuration
- **DATABASE_URL**: URL สำหรับเชื่อมต่อฐานข้อมูล
  - **PostgreSQL**: `postgresql://username:password@hostname:5432/database_name`
    - `username`: ชื่อผู้ใช้ฐานข้อมูล
    - `password`: รหัสผ่านฐานข้อมูล
    - `hostname`: ที่อยู่เซิร์ฟเวอร์ฐานข้อมูล (เช่น `localhost` หรือ IP address)
    - `5432`: พอร์ต PostgreSQL (default)
    - `database_name`: ชื่อฐานข้อมูลที่ต้องการใช้
  - **SQLite** (ไม่แนะนำใน Production): `sqlite:///database.db`
  - **Heroku PostgreSQL**: Heroku จะตั้งค่า `DATABASE_URL` ให้อัตโนมัติ

#### Application Settings
- **MAX_CONTENT_LENGTH**: ขนาดไฟล์สูงสุดที่อนุญาต (bytes) - ค่า default = 16MB
- **UPLOAD_FOLDER**: โฟลเดอร์สำหรับเก็บไฟล์ที่อัปโหลด

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
ถ้าต้องการใช้ไฟล์ `.env` ในการพัฒนาบนเครื่อง Local:

1. ติดตั้ง python-dotenv:
```bash
pip install python-dotenv
```

2. เพิ่มโค้ดใน `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()  # โหลดค่าจากไฟล์ .env
```

## การใช้งาน

### สำหรับผู้ใช้ทั่วไป
1. เข้าสู่เว็บไซต์
2. กรอกข้อมูลในแบบฟอร์ม
3. อัปโหลดเอกสารประกอบ
4. ส่งแบบฟอร์ม

### สำหรับผู้ดูแลระบบ (Admin)
- รหัสผ่าน Admin: `Publication_IRD`
- คลิก "Admin Login" เพื่อเข้าสู่ระบบจัดการ
- ดูข้อมูลที่ส่งเข้ามา
- ดาวน์โหลด PDF รายงาน
- ตั้งค่าระบบ

## โครงสร้างโปรเจค
```
R2R-System/
├── app.py                 # Main Flask application
├── wsgi.py               # WSGI entry point
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment config
├── runtime.txt          # Python version specification
├── static/              # CSS, JS, fonts
├── templates/           # HTML templates
├── uploads/             # File uploads directory
└── instance/           # Database files
```

## ข้อมูลการติดต่อ
สำหรับคำถามหรือปัญหาการใช้งาน กรุณาติดต่อทีมพัฒนา

---
© 2025 มหาวิทยาลัยเทคโนโลยีราชมงคลธัญบุรี
