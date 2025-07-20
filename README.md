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
