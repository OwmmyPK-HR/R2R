# 📚 คู่มือการจัดการฐานข้อมูล R2R System

ระบบคำขอค่าตอบแทนผลงานตีพิมพ์และผลงานสร้างสรรค์

---

## 📋 สารบัญ

1. [ภาพรวมระบบฐานข้อมูล](#ภาพรวมระบบฐานข้อมูล)
2. [โครงสร้างตาราง](#โครงสร้างตาราง)
3. [วิธีการสร้างฐานข้อมูล](#วิธีการสร้างฐานข้อมูล)
4. [การใช้งานสคริปต์](#การใช้งานสคริปต์)
5. [การ Migration](#การ-migration)
6. [คำสั่งที่เป็นประโยชน์](#คำสั่งที่เป็นประโยชน์)

---

## 🗄️ ภาพรวมระบบฐานข้อมูล

ระบบ R2R รองรับฐานข้อมูล 2 ประเภท:

- **SQLite** - สำหรับการพัฒนาและทดสอบในเครื่อง (Local Development)
- **PostgreSQL** - สำหรับการใช้งานจริง (Production) บน Heroku หรือ Server

### ตารางในระบบ

| ตาราง | จุดประสงค์ | จำนวนฟิลด์ |
|--------|------------|-----------|
| **submission** | เก็บข้อมูลการยื่นคำขอทั้งหมด | 80+ ฟิลด์ |
| **settings** | เก็บการตั้งค่าค่าตอบแทนและการตั้งค่าอื่นๆ | 4 ฟิลด์ |

---

## 📊 โครงสร้างตาราง

### 1. ตาราง `submission`

เก็บข้อมูลการยื่นคำขอค่าตอบแทน แบ่งเป็น 7 ส่วน:

#### Part 1: ข้อมูลผู้ยื่นคำขอ
- `id` - รหัสคำขอ (Primary Key)
- `created_at` - วันเวลาที่ส่งคำขอ
- `full_name` - ชื่อ-นามสกุล
- `academic_position` - ตำแหน่งวิชาการ
- `affiliation` - สังกัด
- `phone` - โทรศัพท์
- `mobile_phone` - โทรศัพท์มือถือ
- `email` - อีเมล

#### Part 2: ข้อมูลผลงาน
- `work_name_th` - ชื่อผลงาน (ไทย)
- `work_name_en` - ชื่อผลงาน (อังกฤษ)
- `funding_source` - แหล่งทุน
- `fiscal_year` - ปีงบประมาณ
- `project_name` - ชื่อโครงการวิจัย
- `qual_1_1`, `qual_1_2`, `qual_1_3` - คุณสมบัติผลงาน
- `scope_2_1`, `scope_2_2`, `scope_2_3` - ขอบเขตการขอรับเงิน
- `payment_3_1`, `payment_3_2`, `payment_3_3` - ประเภทการชำระเงิน
- `page_charge_amount` - จำนวนเงิน Page Charge
- `num_institutes_3_3` - จำนวนสถาบัน
- `share_amount_3_3` - จำนวนเงินที่แบ่ง

#### Part 4: ค่าตอบแทนวารสารระดับนานาชาติ
- `charge_int_checkbox` - เลือกขอค่า Page Charge
- `charge_int_amount` - จำนวนเงินค่า Page Charge
- `remuneration_int_checkbox` - เลือกขอค่าตอบแทนนานาชาติ
- `international_quartile` - Quartile (Q1/Q2/Q3/Q4)
- `share_int_checkbox` - มีการแบ่งหรือไม่
- `share_int_base_amount` - จำนวนเงินฐาน
- `share_int_num_institutes` - จำนวนสถาบันที่แบ่ง
- `share_int_final_amount` - จำนวนเงินสุดท้าย

#### Part 5: วารสารพิเศษ (Editorial Board)
- `special_nat_checkbox` - วารสารพิเศษระดับชาติ
- `special_nat_share_*` - ข้อมูลการแบ่งเงิน
- `special_int_checkbox` - วารสารพิเศษระดับนานาชาติ
- `special_international_quartile` - Quartile
- `special_int_share_*` - ข้อมูลการแบ่งเงิน

#### Part 6: ผลงานสร้างสรรค์
- `creative_level_asean` - ระดับอาเซียน
- `creative_level_inter_coop` - ระดับความร่วมมือนานาชาติ
- `creative_level_national` - ระดับชาติ
- `creative_level_institutional` - ระดับสถาบัน
- `creative_level_public` - ระดับเผยแพร่สู่สาธารณะ
- `creative_share_*` - ข้อมูลการแบ่งเงิน

#### Part 7: หลักฐานประกอบ
- `evidence_*_check` - เลือกส่งเอกสารหรือไม่
- `evidence_*_upload` - ชื่อไฟล์ที่อัพโหลด
  - Page Charge
  - Full Paper
  - Consent Letter
  - Quartile
  - TCI
  - Editorial Board
  - Exhibition
  - Proof
  - NRMS
  - Other

### 2. ตาราง `settings`

เก็บการตั้งค่าต่างๆ ของระบบ

- `id` - รหัสการตั้งค่า (Primary Key)
- `key` - ชื่อคีย์ของการตั้งค่า (Unique)
- `value` - ค่าที่ตั้งไว้
- `updated_at` - วันเวลาที่อัพเดทล่าสุด

#### ตัวอย่างการตั้งค่าเริ่มต้น:
```
page_charge_rate = 10000
int_journal_rate = 15000
int_journal_q1q2_rate = 20000
special_nat_rate = 12000
special_int_rate = 18000
creative_asean_rate = 15000
creative_inter_coop_rate = 12000
creative_national_rate = 10000
creative_institutional_rate = 8000
creative_public_rate = 5000
```

---

## 🚀 วิธีการสร้างฐานข้อมูล

### วิธีที่ 1: ใช้สคริปต์ Python (แนะนำ)

#### สร้างฐานข้อมูลใหม่:
```powershell
# ไปที่โฟลเดอร์ db
cd g:\IRD\R2R\01. R2R-Sytem\db

# รันสคริปต์
python init_db.py
```

#### รีเซ็ตฐานข้อมูล (ลบและสร้างใหม่):
```powershell
python init_db.py --reset
```

### วิธีที่ 2: ใช้ Python Flask Shell

```powershell
# ไปที่โฟลเดอร์หลัก
cd g:\IRD\R2R\01. R2R-Sytem

# เปิด Flask shell
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✅ สร้างฐานข้อมูลสำเร็จ!')"
```

### วิธีที่ 3: รัน SQL โดยตรง (สำหรับ SQLite)

```powershell
# ติดตั้ง sqlite3 (ถ้ายังไม่มี)
# สำหรับ Windows: ดาวน์โหลดจาก https://www.sqlite.org/download.html

# รัน SQL script
sqlite3 instance\database.db < db\schema.sql
```

### วิธีที่ 4: รัน SQL โดยตรง (สำหรับ PostgreSQL)

```bash
# เชื่อมต่อกับ PostgreSQL
psql -U username -d database_name -f db/schema_postgres.sql

# หรือถ้าใช้ Heroku
heroku pg:psql -a your-app-name < db/schema_postgres.sql
```

---

## 🔧 การใช้งานสคริปต์

### init_db.py

สคริปต์หลักสำหรับจัดการฐานข้อมูล

#### คำสั่งพื้นฐาน:

```powershell
# สร้างฐานข้อมูลใหม่
python db\init_db.py

# รีเซ็ตฐานข้อมูล
python db\init_db.py --reset

# ดูความช่วยเหลือ
python db\init_db.py --help
```

#### ฟังก์ชันที่มีใน init_db.py:

1. **init_database()** - สร้างตารางทั้งหมดและตั้งค่าเริ่มต้น
2. **drop_all_tables()** - ลบตารางทั้งหมด
3. **reset_database()** - รีเซ็ตฐานข้อมูลใหม่ทั้งหมด

---

## 🔄 การ Migration

เมื่อมีการเปลี่ยนแปลงโครงสร้างฐานข้อมูล ใช้สคริปต์ migration:

### ตัวอย่าง Migration Scripts ที่มีอยู่:

1. **migrate_database.py** - เพิ่มฟิลด์ `scope_2_3`

### วิธีการรัน Migration:

```powershell
# Migration: เพิ่มฟิลด์ scope_2_3
python migrate_database.py
```

### สร้าง Migration Script ใหม่:

```python
# template_migration.py
from app import app, db
from sqlalchemy import text

def add_new_field():
    """เพิ่มฟิลด์ใหม่ลงในตาราง"""
    with app.app_context():
        try:
            database_url = app.config['SQLALCHEMY_DATABASE_URI']
            
            if database_url.startswith('sqlite'):
                # สำหรับ SQLite
                result = db.session.execute(text("PRAGMA table_info(submission)")).fetchall()
                columns = [row[1] for row in result]
                
                if 'new_field_name' not in columns:
                    db.session.execute(text(
                        "ALTER TABLE submission ADD COLUMN new_field_name VARCHAR(50)"
                    ))
                    db.session.commit()
                    print("✅ เพิ่มฟิลด์สำเร็จ!")
            else:
                # สำหรับ PostgreSQL
                result = db.session.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='submission' AND column_name='new_field_name'
                """)).fetchall()
                
                if not result:
                    db.session.execute(text(
                        "ALTER TABLE submission ADD COLUMN new_field_name VARCHAR(50)"
                    ))
                    db.session.commit()
                    print("✅ เพิ่มฟิลด์สำเร็จ!")
                    
        except Exception as e:
            db.session.rollback()
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return False
        
        return True

if __name__ == '__main__':
    add_new_field()
```

---

## 💡 คำสั่งที่เป็นประโยชน์

### ตรวจสอบข้อมูลในฐานข้อมูล (SQLite):

```powershell
# เปิด SQLite shell
sqlite3 instance\database.db

# ดูรายชื่อตารางทั้งหมด
.tables

# ดูโครงสร้างตาราง
.schema submission

# นับจำนวนข้อมูลในตาราง
SELECT COUNT(*) FROM submission;

# ดูข้อมูล 10 รายการล่าสุด
SELECT id, full_name, created_at FROM submission ORDER BY created_at DESC LIMIT 10;

# ออกจาก SQLite
.exit
```

### ตรวจสอบข้อมูลในฐานข้อมูล (PostgreSQL):

```bash
# เชื่อมต่อ PostgreSQL
psql -U username -d database_name

# หรือใช้กับ Heroku
heroku pg:psql -a your-app-name

# ดูรายชื่อตารางทั้งหมด
\dt

# ดูโครงสร้างตาราง
\d submission

# นับจำนวนข้อมูล
SELECT COUNT(*) FROM submission;

# ออกจาก psql
\q
```

### สำรองข้อมูล (Backup):

```powershell
# SQLite - คัดลอกไฟล์ database
copy instance\database.db instance\database_backup_$(Get-Date -Format 'yyyyMMdd').db

# PostgreSQL - Export data
pg_dump -U username database_name > backup_$(date +%Y%m%d).sql

# Heroku - Backup
heroku pg:backups:capture -a your-app-name
heroku pg:backups:download -a your-app-name
```

### กู้คืนข้อมูล (Restore):

```powershell
# SQLite - กู้คืนจากไฟล์สำรอง
copy instance\database_backup_20250209.db instance\database.db

# PostgreSQL - Import data
psql -U username -d database_name < backup_20250209.sql

# Heroku - Restore
heroku pg:backups:restore backup-url DATABASE_URL -a your-app-name
```

---

## 🔍 แก้ไขปัญหาที่พบบ่อย

### 1. ฐานข้อมูลไม่ถูกสร้าง

**ปัญหา:** รันสคริปต์แล้วไม่มีไฟล์ database.db

**วิธีแก้:**
```powershell
# ตรวจสอบว่าโฟลเดอร์ instance มีอยู่หรือไม่
mkdir instance -Force

# รันสคริปต์อีกครั้ง
python db\init_db.py
```

### 2. Error: Table already exists

**ปัญหา:** ตารางถูกสร้างไปแล้ว

**วิธีแก้:**
- ถ้าต้องการสร้างใหม่: `python db\init_db.py --reset`
- ถ้าต้องการเพิ่มฟิลด์ใหม่: ใช้ migration script

### 3. Permission Denied

**ปัญหา:** ไม่มีสิทธิ์เขียนไฟล์

**วิธีแก้:**
```powershell
# รัน PowerShell ในฐานะ Administrator
# หรือเปลี่ยน permission ของโฟลเดอร์
```

### 4. ModuleNotFoundError: No module named 'app'

**ปัญหา:** Python ไม่พบ module app

**วิธีแก้:**
```powershell
# ไปที่โฟลเดอร์หลักของโปรเจค
cd g:\IRD\R2R\01. R2R-Sytem

# แล้วรันจากโฟลเดอร์หลัก
python db\init_db.py
```

---

## 📝 หมายเหตุสำคัญ

1. **สำรองข้อมูลก่อนทำ Migration** - ข้อมูลอาจสูญหายได้
2. **ใช้ SQLite สำหรับการพัฒนา** - ง่ายและรวดเร็ว
3. **ใช้ PostgreSQL สำหรับ Production** - เสถียรและรองรับผู้ใช้งานพร้อมกันได้มาก
4. **ตรวจสอบ Environment Variable** - สำหรับ DATABASE_URL ใน production
5. **Migration ต้องทำทั้ง Development และ Production** - เพื่อให้โครงสร้างเหมือนกัน

---

## 📞 ติดต่อสอบถาม

หากพบปัญหาในการใช้งาน กรุณาติดต่อทีมพัฒนาระบบ

**สถาบันวิจัยและพัฒนา (IRD)**

---

## 📄 เอกสารอ้างอิง

- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**อัพเดทล่าสุด:** 9 กุมภาพันธ์ 2026

**เวอร์ชัน:** 1.0.0
