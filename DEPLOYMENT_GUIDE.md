# 🚀 คู่มือการ Deploy ระบบ R2R สู่ Production

## 📋 สารบัญ
1. [ภาพรวมการ Deploy](#ภาพรวมการ-deploy)
2. [เตรียมความพร้อม](#เตรียมความพร้อม)
3. [การตั้งค่า Environment Variables](#การตั้งค่า-environment-variables)
4. [การเตรียม Database](#การเตรียม-database)
5. [วิธี Deploy แบบต่างๆ](#วิธี-deploy-แบบต่างๆ)
   - [Deploy บน Heroku](#deploy-บน-heroku)
   - [Deploy บน Railway](#deploy-บน-railway)
   - [Deploy บน Render](#deploy-บน-render)
   - [Deploy บน DigitalOcean/VPS](#deploy-บน-digitaloceanvps)
6. [การทำ Database Migration](#การทำ-database-migration)
7. [การตั้งค่าหลัง Deploy](#การตั้งค่าหลัง-deploy)
8. [การตรวจสอบและ Troubleshooting](#การตรวจสอบและ-troubleshooting)
9. [Security Best Practices](#security-best-practices)
10. [การ Backup และ Maintenance](#การ-backup-และ-maintenance)

---

## ภาพรวมการ Deploy

ระบบ R2R เป็น Flask application ที่สามารถ deploy บน platform ต่างๆ ได้ โดยรองรับ:
- **Database**: SQLite (local) / PostgreSQL (production)
- **Web Server**: Gunicorn
- **Python Version**: 3.11.9

### เลือก Platform ที่เหมาะสม

| Platform | ราคา | ความยาก | เหมาะสำหรับ |
|----------|------|---------|-------------|
| Heroku | ฟรี-$7/เดือน | ⭐⭐ | เริ่มต้น, ทดสอบ |
| Railway | ฟรี-$5/เดือน | ⭐⭐ | เริ่มต้น, สะดวกรวดเร็ว |
| Render | ฟรี-$7/เดือน | ⭐⭐ | CI/CD อัตโนมัติ |
| DigitalOcean/VPS | $5+/เดือน | ⭐⭐⭐⭐ | ควบคุมเต็มรูปแบบ |

---

## เตรียมความพร้อม

### ✅ Checklist ก่อน Deploy

- [ ] Git repository พร้อมใช้งาน
- [ ] ทดสอบระบบใน local environment สำเร็จ
- [ ] มี PostgreSQL database พร้อม (สำหรับ production)
- [ ] เตรียม SECRET_KEY สำหรับ production
- [ ] ตั้งค่า `ADMIN_PASSWORD` ใน Environment Variables (ห้ามใช้ค่า default)
- [ ] ตรวจสอบไฟล์ที่จำเป็น: `Procfile`, `requirements.txt`, `runtime.txt`

### 🔧 สร้าง SECRET_KEY ใหม่

เพื่อความปลอดภัย **ห้ามใช้ SECRET_KEY เดิมใน production**

```bash
# วิธีที่ 1: ใช้ Python
python -c "import secrets; print(secrets.token_hex(32))"

# วิธีที่ 2: ใช้ OpenSSL
openssl rand -hex 32
```

คัดลอกผลลัพธ์ที่ได้ไว้ใช้เป็น SECRET_KEY

---

## การตั้งค่า Environment Variables

### 📝 รายการ Environment Variables ที่จำเป็น

#### 1. **SECRET_KEY** (บังคับ)
- **คำอธิบาย**: คีย์ลับสำหรับการเข้ารหัส session และ cookies
- **วิธีสร้าง**: ใช้คำสั่งด้านบน
- **ตัวอย่าง**: `a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456`
- ⚠️ **สำคัญ**: ต้องเปลี่ยนใหม่ทุกครั้งใน production

#### 2. **DATABASE_URL** (บังคับสำหรับ PostgreSQL)
- **คำอธิบาย**: URL สำหรับเชื่อมต่อ PostgreSQL database
- **รูปแบบ**: `postgresql://username:password@hostname:5432/database_name`
- **ตัวอย่าง**: `postgresql://r2r_user:P@ssw0rd123@db.example.com:5432/r2r_db`

#### 3. **FLASK_ENV** (แนะนำ)
- **คำอธิบาย**: สภาพแวดล้อมการทำงาน
- **ค่าที่ใช้**: `production` (สำหรับ production) หรือ `development` (สำหรับ dev)
- **ค่าเริ่มต้น**: production

#### 4. **FLASK_DEBUG** (แนะนำ)
- **คำอธิบาย**: เปิด/ปิด debug mode
- **ค่าที่ใช้**: `0` (ปิด - สำหรับ production) หรือ `1` (เปิด - สำหรับ dev)
- **ค่าเริ่มต้น**: 0

#### 5. **ADMIN_PASSWORD** (แนะนำอย่างยิ่ง)
- **คำอธิบาย**: รหัสผ่านตั้งต้นสำหรับผู้ดูแลระบบ
- **ค่าที่ใช้**: ตั้งเป็นรหัสผ่านใหม่ที่คาดเดายาก (อย่างน้อย 12 ตัวอักษร)
- ⚠️ **สำคัญ**: ใน production หากไม่ตั้งค่า หรือใช้ค่า default ระบบจะไม่ยอมเริ่มทำงาน
- **หมายเหตุ**: หลังระบบ hash รหัสผ่านลงฐานข้อมูลแล้ว การเปลี่ยนค่า env อย่างเดียวจะไม่อัปเดตรหัสผ่านที่ใช้งานอยู่

#### 6. **SESSION_COOKIE_SECURE** (แนะนำอย่างยิ่ง)
- **คำอธิบาย**: บังคับให้ session cookie ส่งผ่าน HTTPS เท่านั้น
- **ค่าที่ใช้**: `1` สำหรับ production ที่มี HTTPS

#### 7. **SESSION_COOKIE_HTTPONLY** (แนะนำ)
- **คำอธิบาย**: ป้องกัน JavaScript ฝั่ง browser ไม่ให้เข้าถึง session cookie
- **ค่าที่ใช้**: `1`

#### 8. **SESSION_COOKIE_SAMESITE** (แนะนำ)
- **คำอธิบาย**: จำกัดการส่ง cookie ข้ามไซต์เพื่อลด CSRF risk
- **ค่าที่ใช้**: `Lax` หรือ `Strict` ตาม flow ที่ต้องการ

#### 9. **PREFERRED_URL_SCHEME** (แนะนำ)
- **คำอธิบาย**: กำหนด scheme หลักของ URL ที่ระบบสร้าง
- **ค่าที่ใช้**: `https`

#### 10. **USE_PROXY_FIX** (ใช้เมื่ออยู่หลัง reverse proxy)
- **คำอธิบาย**: ให้ Flask เคารพ `X-Forwarded-*` headers จาก Nginx, Caddy, Load Balancer หรือ platform proxy
- **ค่าที่ใช้**: `1`

#### 11. **SESSION_LIFETIME_MINUTES** (แนะนำ)
- **คำอธิบาย**: กำหนดอายุ session ของ admin
- **ค่าที่ใช้**: เช่น `480` (8 ชั่วโมง)

#### 12. **LIMITER_STORAGE_URI** (แนะนำอย่างยิ่ง)
- **คำอธิบาย**: backend storage ของ rate limiter
- **ค่าที่ใช้**: `memory://` (single worker) หรือ `redis://host:6379` (multi-worker)

#### 13. **WEB_CONCURRENCY** (แนะนำ)
- **คำอธิบาย**: จำนวน Gunicorn workers
- **ค่าที่ใช้**: `1` เมื่อใช้ `LIMITER_STORAGE_URI=memory://`

### 📄 ตัวอย่างไฟล์ .env (สำหรับ VPS/Server เอง)

```bash
# Flask Configuration
SECRET_KEY=a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456
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

# Database Configuration
DATABASE_URL=postgresql://r2r_user:YourSecurePassword@localhost:5432/r2r_production

# Admin Configuration
ADMIN_PASSWORD=change-this-admin-password

# Application Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
SESSION_LIFETIME_MINUTES=480

# Rate Limiter
LIMITER_STORAGE_URI=memory://
WEB_CONCURRENCY=1
```

---

## การเตรียม Database

### 🗄️ SQLite vs PostgreSQL

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| ใช้สำหรับ | Development, Testing | Production |
| ประสิทธิภาพ | ปานกลาง | สูง |
| Concurrent Users | จำกัด | ไม่จำกัด |
| Backup | คัดลอกไฟล์ | pg_dump, pg_restore |

### 🐘 ติดตั้ง PostgreSQL

#### บน Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### บนเครื่อง Local (Windows):
1. ดาวน์โหลดจาก https://www.postgresql.org/download/windows/
2. ติดตั้งและจดจำรหัสผ่าน postgres user

#### บนเครื่อง Local (macOS):
```bash
brew install postgresql
brew services start postgresql
```

### 📊 สร้าง Database และ User

```bash
# เข้าสู่ PostgreSQL
sudo -u postgres psql

# สร้าง database user
CREATE USER r2r_user WITH PASSWORD 'YourSecurePassword';

# สร้าง database
CREATE DATABASE r2r_production;

# ให้สิทธิ์
GRANT ALL PRIVILEGES ON DATABASE r2r_production TO r2r_user;

# ออกจาก psql
\q
```

### 🔄 Initialize Database

โปรเจคปัจจุบันตั้งค่าให้เริ่มฐานข้อมูลอัตโนมัติแล้ว:

- ใช้ `release: python migrate_database.py` ใน `Procfile`
- และมี `_run_auto_migration()` ในแอปเพื่อช่วยเพิ่มคอลัมน์ที่ขาดเมื่อเริ่มระบบ

กรณีต้องการ initialize/manual เพิ่มเติม สามารถรันได้:

```bash
python db/init_db.py
```

---

## วิธี Deploy แบบต่างๆ

## Deploy บน Heroku

### 🟣 ขั้นตอนที่ 1: เตรียม Heroku CLI

```bash
# ติดตั้ง Heroku CLI
# Windows: ดาวน์โหลดจาก https://devcenter.heroku.com/articles/heroku-cli
# macOS:
brew tap heroku/brew && brew install heroku
# Ubuntu:
curl https://cli-assets.heroku.com/install.sh | sh

# Login เข้า Heroku
heroku login
```

### 🟣 ขั้นตอนที่ 2: สร้าง Heroku App

```bash
# สร้าง app ใหม่
heroku create r2r-system-ird
# หรือใช้ชื่อที่ต้องการ
heroku create your-app-name

# ตรวจสอบ remote git ถูกเพิ่มแล้ว
git remote -v
```

### 🟣 ขั้นตอนที่ 3: เพิ่ม PostgreSQL Add-on

```bash
# เพิ่ม PostgreSQL (ฟรี - Hobby Dev)
heroku addons:create heroku-postgresql:essential-0

# ตรวจสอบ DATABASE_URL
heroku config:get DATABASE_URL
```

### 🟣 ขั้นตอนที่ 4: ตั้งค่า Environment Variables

```bash
# ตั้งค่า SECRET_KEY (สร้างใหม่ก่อน!)
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# ตั้งค่า FLASK_ENV
heroku config:set FLASK_ENV=production

# ตั้งค่าเพิ่มเติมให้ตรงโปรเจคปัจจุบัน
heroku config:set APP_ENV=production SESSION_LIFETIME_MINUTES=480 LIMITER_STORAGE_URI=memory:// WEB_CONCURRENCY=1

# ตรวจสอบ config ทั้งหมด
heroku config
```

### 🟣 ขั้นตอนที่ 5: Deploy โค้ด

```bash
# Commit โค้ดทั้งหมด (ถ้ายังไม่ได้ commit)
git add .
git commit -m "Ready for production deployment"

# Push ไปยัง Heroku
git push heroku main
# หรือถ้าใช้ branch master
git push heroku master
```

### 🟣 ขั้นตอนที่ 6: สร้าง Database Tables

โดยปกติ Heroku จะรัน `release` command ใน `Procfile` ให้อัตโนมัติ (`python migrate_database.py`)

หากต้องการสั่งเองเพิ่มเติม:

```bash
heroku run python db/init_db.py
```

### 🟣 ขั้นตอนที่ 7: เปิดเว็บไซต์

```bash
# เปิด browser ไปยัง app
heroku open

# ดู logs
heroku logs --tail
```

### 🔧 คำสั่งที่ใช้บ่อยบน Heroku

```bash
# ดู logs แบบ real-time
heroku logs --tail

# Restart app
heroku restart

# เข้าถึง console
heroku run bash

# ดู config vars
heroku config

# ตั้งค่าใหม่
heroku config:set KEY=VALUE

# ลบ config
heroku config:unset KEY

# ดูข้อมูล app
heroku info

# ดู database info
heroku pg:info

# Backup database
heroku pg:backups:capture
heroku pg:backups:download
```

---

## Deploy บน Railway

### 🚂 ขั้นตอนที่ 1: สร้างบัญชี Railway

1. ไปที่ https://railway.app/
2. Sign up ด้วย GitHub account
3. Verify email

### 🚂 ขั้นตอนที่ 2: Push โค้ดไปยัง GitHub

```bash
# สร้าง repository ใหม่บน GitHub
# จากนั้น push โค้ด
git remote add origin https://github.com/your-username/r2r-system.git
git add .
git commit -m "Initial commit for Railway deployment"
git push -u origin main
```

### 🚂 ขั้นตอนที่ 3: Deploy จาก GitHub

1. ใน Railway Dashboard คลิก **"New Project"**
2. เลือก **"Deploy from GitHub repo"**
3. เลือก repository ของคุณ
4. Railway จะ detect Python project อัตโนมัติ

### 🚂 ขั้นตอนที่ 4: เพิ่ม PostgreSQL Database

1. ใน Project คลิก **"+ New"**
2. เลือก **"Database"** → **"Add PostgreSQL"**
3. Railway จะสร้าง database และเพิ่ม `DATABASE_URL` ให้อัตโนมัติ

### 🚂 ขั้นตอนที่ 5: ตั้งค่า Environment Variables

1. คลิกที่ service ของคุณ
2. ไปที่แท็บ **"Variables"**
3. เพิ่ม variables:
   - `SECRET_KEY`: [คีย์ที่สร้างใหม่]
   - `FLASK_ENV`: `production`
    - `APP_ENV`: `production`
    - `SESSION_LIFETIME_MINUTES`: `480`
    - `LIMITER_STORAGE_URI`: `memory://`
    - `WEB_CONCURRENCY`: `1`
   - **DATABASE_URL จะถูกเพิ่มอัตโนมัติ**

### 🚂 ขั้นตอนที่ 6: สร้าง Database Tables

1. ไปที่แท็บ **"Settings"**
2. หาส่วน **"Deploy"** → คลิก **"Deploy"**
3. หลัง deploy เสร็จ ไปที่แท็บ **"Deployments"**
4. คลิก **"View Logs"** เพื่อดู output

หรือใช้ **Railway CLI**:

```bash
# ติดตั้ง Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link กับ project
railway link

# Run command (ถ้าต้องการสั่งเอง)
railway run python db/init_db.py
```

หมายเหตุ: ถ้า Railway รองรับ `release` command จาก `Procfile` จะรัน `python migrate_database.py` ให้อัตโนมัติ

### 🚂 ขั้นตอนที่ 7: เปิดเว็บไซต์

1. ใน service settings ไปที่ **"Settings"** → **"Networking"**
2. คลิก **"Generate Domain"**
3. จะได้ URL เช่น `your-app.up.railway.app`

---

## Deploy บน Render

### 🎨 ขั้นตอนที่ 1: สร้างบัญชี Render

1. ไปที่ https://render.com/
2. Sign up ด้วย GitHub account

### 🎨 ขั้นตอนที่ 2: สร้าง PostgreSQL Database

1. จาก Dashboard คลิก **"New +"**
2. เลือก **"PostgreSQL"**
3. ตั้งค่า:
   - **Name**: `r2r-database`
   - **Database**: `r2r_production`
   - **User**: `r2r_user`
   - **Region**: เลือกใกล้เคียง
   - **Plan**: Free
4. คลิก **"Create Database"**
5. **บันทึก Internal Database URL** สำหรับใช้ใน web service

### 🎨 ขั้นตอนที่ 3: สร้าง Web Service

1. คลิก **"New +"** → **"Web Service"**
2. เลือก **"Build and deploy from a Git repository"**
3. Connect GitHub repository ของคุณ
4. ตั้งค่า:
   - **Name**: `r2r-system`
   - **Region**: เลือกเดียวกับ database
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn wsgi:app --workers ${WEB_CONCURRENCY:-1} --timeout 120 --bind 0.0.0.0:${PORT:-8000}`

### 🎨 ขั้นตอนที่ 4: ตั้งค่า Environment Variables

ใน Web Service Settings → **"Environment"** เพิ่ม:

```
SECRET_KEY=[คีย์ที่สร้างใหม่]
DATABASE_URL=[Internal Database URL จากขั้นตอนที่ 2]
FLASK_ENV=production
APP_ENV=production
SESSION_LIFETIME_MINUTES=480
LIMITER_STORAGE_URI=memory://
WEB_CONCURRENCY=1
```

### 🎨 ขั้นตอนที่ 5: Deploy

1. คลิก **"Create Web Service"**
2. Render จะ build และ deploy อัตโนมัติ
3. ดู logs ในแท็บ **"Logs"**

### 🎨 ขั้นตอนที่ 6: สร้าง Database Tables

ใช้ **Shell** feature:

1. ใน Web Service ไปที่ **"Shell"**
2. รันคำสั่ง:
```bash
python db/init_db.py
```

หมายเหตุ: หาก Render รัน `release` command จาก `Procfile` ได้ ระบบจะ migrate ให้อัตโนมัติอยู่แล้ว

### 🎨 ขั้นตอนที่ 7: เข้าถึงเว็บไซต์

ไปที่ URL ที่แสดงด้านบน เช่น `https://r2r-system.onrender.com`

---

## Deploy บน DigitalOcean/VPS

### 💧 ขั้นตอนที่ 1: เตรียม VPS

1. สร้าง Droplet บน DigitalOcean (หรือ VPS จาก provider อื่น)
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic - $6/month
   - **Region**: ใกล้ผู้ใช้งาน
2. เพิ่ม SSH key หรือใช้ password
3. บันทึก IP address

### 💧 ขั้นตอนที่ 2: เชื่อมต่อ VPS

```bash
# เชื่อมต่อผ่าน SSH
ssh root@your_server_ip

# Update packages
apt update && apt upgrade -y
```

### 💧 ขั้นตอนที่ 3: ติดตั้ง Dependencies

```bash
# ติดตั้ง Python และ tools
apt install python3 python3-pip python3-venv git nginx postgresql postgresql-contrib -y

# ติดตั้ง supervisor สำหรับจัดการ process
apt install supervisor -y
```

### 💧 ขั้นตอนที่ 4: ตั้งค่า PostgreSQL

```bash
# เข้าสู่ PostgreSQL
sudo -u postgres psql

# ใน psql prompt:
CREATE DATABASE r2r_production;
CREATE USER r2r_user WITH PASSWORD 'YourSecurePassword123!';
GRANT ALL PRIVILEGES ON DATABASE r2r_production TO r2r_user;
ALTER DATABASE r2r_production OWNER TO r2r_user;
\q
```

### 💧 ขั้นตอนที่ 5: Clone โปรเจค

```bash
# สร้าง user สำหรับ app (แนะนำ - ไม่ควรใช้ root)
adduser r2rapp
usermod -aG sudo r2rapp
su - r2rapp

# Clone repository
cd /home/r2rapp
git clone https://github.com/your-username/r2r-system.git
cd r2r-system
```

### 💧 ขั้นตอนที่ 6: ตั้งค่า Virtual Environment

```bash
# สร้าง virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# ติดตั้ง dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 💧 ขั้นตอนที่ 7: ตั้งค่า Environment Variables

```bash
# สร้างไฟล์ .env
nano .env

# เพิ่มเนื้อหา:
SECRET_KEY=your-generated-secret-key-here
DATABASE_URL=postgresql://r2r_user:YourSecurePassword123!@localhost:5432/r2r_production
FLASK_ENV=production
APP_ENV=production
FLASK_DEBUG=0
ADMIN_PASSWORD=change-this-admin-password
SESSION_LIFETIME_MINUTES=480
LIMITER_STORAGE_URI=memory://
WEB_CONCURRENCY=1

# บันทึก (Ctrl+X, Y, Enter)

# ป้องกันไฟล์ .env
chmod 600 .env
```

### 💧 ขั้นตอนที่ 8: Initialize Database

```bash
# ยังคง activate venv อยู่
python db/init_db.py
```

### 💧 ขั้นตอนที่ 9: ทดสอบรัน Gunicorn

```bash
# ทดสอบ
gunicorn --bind 0.0.0.0:8000 wsgi:app

# ถ้าทำงานได้ ให้กด Ctrl+C เพื่อหยุด
```

### 💧 ขั้นตอนที่ 10: ตั้งค่า Supervisor

```bash
# กลับมาเป็น root
exit

# สร้างไฟล์ config
nano /etc/supervisor/conf.d/r2r.conf
```

เพิ่มเนื้อหา:

```ini
[program:r2r]
directory=/home/r2rapp/r2r-system
command=/home/r2rapp/r2r-system/venv/bin/gunicorn --workers 1 --timeout 120 --bind 0.0.0.0:8000 wsgi:app
user=r2rapp
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/r2r/r2r.err.log
stdout_logfile=/var/log/r2r/r2r.out.log
environment=PATH="/home/r2rapp/r2r-system/venv/bin"
```

สร้างโฟลเดอร์ logs:

```bash
mkdir -p /var/log/r2r
chown -R r2rapp:r2rapp /var/log/r2r

# Reload supervisor
supervisorctl reread
supervisorctl update
supervisorctl start r2r
supervisorctl status
```

### 💧 ขั้นตอนที่ 11: ตั้งค่า Nginx

```bash
# สร้างไฟล์ config
nano /etc/nginx/sites-available/r2r
```

เพิ่มเนื้อหา:

```nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;  # เปลี่ยนเป็น domain ของคุณ

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/r2rapp/r2r-system/static;
        expires 30d;
    }

    location /uploads {
        alias /home/r2rapp/r2r-system/uploads;
        expires 7d;
    }

    client_max_body_size 16M;
}
```

Enable site:

```bash
# สร้าง symbolic link
ln -s /etc/nginx/sites-available/r2r /etc/nginx/sites-enabled/

# ลบ default site
rm /etc/nginx/sites-enabled/default

# ทดสอบ config
nginx -t

# Restart nginx
systemctl restart nginx
```

### 💧 ขั้นตอนที่ 12: ตั้งค่า SSL (HTTPS) ด้วย Let's Encrypt

```bash
# ติดตั้ง Certbot
apt install certbot python3-certbot-nginx -y

# รัน Certbot (เปลี่ยน email และ domain)
certbot --nginx -d your_domain.com -d www.your_domain.com

# ข้อมูลที่ต้องกรอก:
# - Email: your-email@example.com
# - Agree to Terms: Yes
# - Redirect HTTP to HTTPS: Yes (แนะนำ)

# ตั้งค่า auto-renewal
systemctl status certbot.timer
```

### 💧 ขั้นตอนที่ 13: ตั้งค่า Firewall

```bash
# Enable UFW firewall
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable

# ตรวจสอบ status
ufw status
```

### 💧 ขั้นตอนที่ 14: เข้าถึงเว็บไซต์

เปิด browser ไปที่:
- `http://your_domain.com` (จะ redirect ไป HTTPS)
- `https://your_domain.com`

### 🔧 คำสั่งที่ใช้บ่อยบน VPS

```bash
# ดู supervisor logs
tail -f /var/log/r2r/r2r.out.log
tail -f /var/log/r2r/r2r.err.log

# ควบคุม app
supervisorctl status r2r
supervisorctl stop r2r
supervisorctl start r2r
supervisorctl restart r2r

# ดู nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Restart services
systemctl restart nginx
systemctl restart supervisor

# Update code
su - r2rapp
cd r2r-system
git pull
source venv/bin/activate
pip install -r requirements.txt
exit
supervisorctl restart r2r
```

---

## การทำ Database Migration

### 🔄 เมื่อมีการเปลี่ยนแปลง Schema

โปรเจคปัจจุบันใช้แนวทาง migration แบบ script/manual เป็นหลัก (`migrate_database.py` + auto migration ในแอป)

#### วิธีที่ 1: ใช้สคริปต์ที่มีอยู่แล้ว

```bash
python migrate_database.py
```

#### วิธีที่ 2: Manual Migration

**สร้างไฟล์ migration script**:

```python
# db/migrations/add_new_field.py
from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        # เพิ่ม column ใหม่
        db.session.execute(text('''
            ALTER TABLE submission 
            ADD COLUMN new_field VARCHAR(200);
        '''))
        db.session.commit()
        print("Migration completed successfully!")

if __name__ == '__main__':
    migrate()
```

**รัน migration**:

```bash
python db/migrations/add_new_field.py
```

### 📦 Backup ก่อน Migration

```bash
# PostgreSQL
pg_dump -U r2r_user -d r2r_production > backup_before_migration.sql

# SQLite
cp instance/database.db instance/database_backup.db
```

---

## การตั้งค่าหลัง Deploy

### ✅ Checklist หลัง Deploy

- [ ] ทดสอบการเข้าถึงหน้าหลัก
- [ ] ทดสอบการล็อกอิน Admin
- [ ] ทดสอบการกรอกฟอร์ม
- [ ] ทดสอบการอัปโหลดไฟล์
- [ ] ทดสอบการสร้าง PDF
- [ ] ตรวจสอบ logs ไม่มี error
- [ ] เปลี่ยนรหัสผ่าน Admin ผ่านหน้า Admin Settings (ถ้าต้องการหมุนรหัส)
- [ ] ตั้งค่า backup อัตโนมัติ
- [ ] ตั้งค่า monitoring
- [ ] เพิ่ม custom domain (ถ้ามี)

### 🔐 เปลี่ยนรหัสผ่าน Admin

ตั้งค่าเริ่มต้นผ่าน Environment Variable (แนะนำ):

```python
# ในไฟล์ app.py
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Publication_IRD')

# ตั้งค่าใน platform
heroku config:set ADMIN_PASSWORD=YourStrongPassword
railway variables set ADMIN_PASSWORD=YourStrongPassword
```

หลังจากระบบเริ่มใช้งานแล้ว สามารถเปลี่ยนรหัสผ่านได้จากหน้า `Admin Settings` โดยไม่ต้องแก้โค้ด

### 📧 ตั้งค่าการแจ้งเตือน (Optional)

เพิ่มฟีเจอร์ส่ง email แจ้งเตือนเมื่อมีการส่งฟอร์ม:

```bash
# เพิ่มใน requirements.txt
Flask-Mail==0.9.1
```

### 🌐 เพิ่ม Custom Domain

#### บน Heroku:
```bash
heroku domains:add www.yourdomain.com
# ตั้งค่า CNAME record ที่ DNS provider ชี้ไปยัง [app-name].herokuapp.com
```

#### บน Railway:
1. Settings → Custom Domain
2. เพิ่ม domain
3. ตั้งค่า CNAME ตามคำแนะนำ

#### บน VPS:
แก้ไข `/etc/nginx/sites-available/r2r`:
```nginx
server_name yourdomain.com www.yourdomain.com;
```

---

## การตรวจสอบและ Troubleshooting

### 🔍 ตรวจสอบ Health Check

**สร้างหน้า health check endpoint**:

แก้ไข `app.py` เพิ่ม:

```python
@app.route('/health')
def health_check():
    try:
        # ทดสอบ database connection
        db.session.execute(text('SELECT 1'))
        db_status = 'ok'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    })
```

**ทดสอบ**:
```bash
curl https://your-app.com/health
```

### 🐛 แก้ปัญหาที่พบบ่อย

#### ปัญหา: Application Error หรือ 500 Error

```bash
# ดู logs
heroku logs --tail  # Heroku
railway logs       # Railway

# ตรวจสอบ:
# 1. DATABASE_URL ถูกต้องหรือไม่
# 2. SECRET_KEY ถูกตั้งค่าหรือไม่
# 3. Dependencies ครบหรือไม่ (requirements.txt)
```

#### ปัญหา: Database Connection Error

```bash
# ตรวจสอบ DATABASE_URL format
# ต้องเป็น postgresql:// ไม่ใช่ postgres://

# แก้ไขใน app.py (มีอยู่แล้ว):
database_url = os.environ.get('DATABASE_URL')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace('postgres://', 'postgresql://')
```

#### ปัญหา: Static Files ไม่โหลด

```bash
# ตรวจสอบ path ใน templates
# ใช้ url_for('static', filename='...')

# ตัวอย่าง:
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

# บน VPS ตรวจสอบ nginx config:
location /static {
    alias /path/to/your/app/static;
}
```

#### ปัญหา: Upload Files หายไป

```bash
# บน Heroku/Railway: ใช้ cloud storage (S3, Cloudinary)
# หรือ persistent volume

# บน VPS: ตรวจสอบ permissions
sudo chown -R r2rapp:r2rapp /home/r2rapp/r2r-system/uploads
```

#### ปัญหา: Memory Exceeded

```bash
# ถ้าใช้ LIMITER_STORAGE_URI=memory:// ให้ WEB_CONCURRENCY=1
# ถ้าต้องการหลาย worker ให้เปลี่ยนเป็น Redis ก่อน
LIMITER_STORAGE_URI=redis://your-redis-host:6379
WEB_CONCURRENCY=2
```

### 📊 Monitoring และ Logging

**เพิ่ม Request Logging**:

```python
# ใน app.py
import logging
from logging.handlers import RotatingFileHandler

# ตั้งค่า logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/r2r.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('R2R startup')
```

**ใช้ Monitoring Services**:

- **Sentry**: Error tracking - https://sentry.io/
- **New Relic**: Performance monitoring - https://newrelic.com/
- **Uptime Robot**: Uptime monitoring - https://uptimerobot.com/

---

## Security Best Practices

### 🔒 Checklist ความปลอดภัย

- [ ] ✅ ใช้ HTTPS (SSL/TLS)
- [ ] ✅ SECRET_KEY ไม่ใช้ค่าเดิม hard-coded
- [ ] ✅ รหัสผ่าน Admin แข็งแกร่งและไม่เปิดเผย
- [ ] ✅ Database credentials ปลอดภัย
- [ ] ✅ ไม่ commit .env ไปใน git
- [ ] ✅ ตั้งค่า CORS อย่างเหมาะสม
- [ ] ✅ Validate ข้อมูล input ทั้งหมด
- [ ] ✅ จำกัดขนาดไฟล์อัปโหลด
- [ ] ✅ ตรวจสอบประเภทไฟล์ที่อัปโหลด
- [ ] ✅ ตั้งค่า `SESSION_LIFETIME_MINUTES` ให้เหมาะกับนโยบายองค์กร
- [ ] ✅ ถ้าต้องการ multi-worker ให้ใช้ Redis กับ Rate Limiter
- [ ] ✅ เปิด firewall บน VPS
- [ ] ✅ Update packages เป็นประจำ

### 🛡️ เพิ่ม Security Headers

เพิ่มใน `app.py`:

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "script-src 'self' 'unsafe-inline'; "
        "font-src 'self' data: https://cdnjs.cloudflare.com; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'"
    )
    # ควรตั้งค่าเฉพาะเมื่อ request มาผ่าน HTTPS
    if request.is_secure:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### 🔐 เข้ารหัสรหัสผ่าน Admin

แทนที่จะใช้ plain text:

```python
from werkzeug.security import generate_password_hash, check_password_hash

# สร้าง hash password (รันครั้งเดียว)
hashed = generate_password_hash('YourAdminPassword')
print(hashed)  # เก็บค่านี้ไว้

# ใช้งาน
ADMIN_PASSWORD_HASH = 'pbkdf2:sha256:...'  # ค่าที่ได้จากด้านบน

# ในฟังก์ชัน login:
if check_password_hash(ADMIN_PASSWORD_HASH, password):
    # Login success
```

### 🗂️ .gitignore ที่ควรมี

ตรวจสอบไฟล์ `.gitignore`:

```gitignore
# Environment
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3
instance/

# Uploads
uploads/*
!uploads/.gitkeep

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## การ Backup และ Maintenance

### 💾 การ Backup Database

#### Heroku:

```bash
# Manual backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download

# กำหนด auto-backup (ต้องอัพเกรด plan)
# Hobby plan ขึ้นไป มี daily backup อัตโนมัติ
```

#### Railway/Render:

ใช้ `pg_dump` ผ่าน CLI หรือสร้าง cron job

#### VPS/DigitalOcean:

**สร้าง Backup Script** (`/home/r2rapp/backup.sh`):

```bash
#!/bin/bash
# R2R Database Backup Script

BACKUP_DIR="/home/r2rapp/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="r2r_production"
DB_USER="r2r_user"

# สร้างโฟลเดอร์ backup ถ้าไม่มี
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U $DB_USER -d $DB_NAME > $BACKUP_DIR/r2r_backup_$DATE.sql

# Compress
gzip $BACKUP_DIR/r2r_backup_$DATE.sql

# ลบ backup เก่าที่เก็บไว้เกิน 30 วัน
find $BACKUP_DIR -type f -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: r2r_backup_$DATE.sql.gz"
```

**ทำให้รันได้**:

```bash
chmod +x /home/r2rapp/backup.sh
```

**ตั้งค่า Cron Job (รัน backup ทุกวันเวลา 2:00 AM)**:

```bash
crontab -e

# เพิ่มบรรทัด:
0 2 * * * /home/r2rapp/backup.sh >> /var/log/r2r/backup.log 2>&1
```

### 🔄 Restore Database

#### จาก Backup File:

```bash
# Heroku
heroku pg:backups:restore [backup-url] DATABASE_URL

# VPS
gunzip -c r2r_backup_20241201_020000.sql.gz | psql -U r2r_user -d r2r_production
```

### 🧹 Maintenance Tasks

**รายเดือน**:
- ตรวจสอบ disk space
- ตรวจสอบ logs
- ตรวจสอบ backup
- อัพเดต dependencies

**รายไตรมาส**:
- Review security settings
- อัพเดต Python และ packages
- ทำ load testing

**ติดตั้ง Auto-update (VPS)**:

```bash
# ติดตั้ง unattended-upgrades
apt install unattended-upgrades

# Enable
dpkg-reconfigure -plow unattended-upgrades
```

---

## 📚 เอกสารเพิ่มเติม

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Gunicorn Deployment](https://docs.gunicorn.org/en/stable/deploy.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)

---

## 🆘 การขอความช่วยเหลือ

หากพบปัญหาหรือข้อสงสัย:

1. ตรวจสอบ logs ของ application
2. ดู [Troubleshooting](#การตรวจสอบและ-troubleshooting) ในคู่มือนี้
3. ค้นหาใน Documentation ของ Platform ที่ใช้
4. ติดต่อผู้พัฒนาหรือทีม IT Support

---

## ✅ สรุป

คู่มือนี้ครอบคลุมการ Deploy ระบบ R2R บน Platform ต่างๆ:

1. **Heroku** - เหมาะสำหรับเริ่มต้น รวดเร็ว
2. **Railway** - สะดวก Auto-deploy จาก GitHub
3. **Render** - ทางเลือกที่ดี มี free tier
4. **DigitalOcean/VPS** - ควบคุมเต็มรูปแบบ สำหรับ advanced users

เลือก Platform ที่เหมาะกับความต้องการและระดับทักษะของคุณ

**สำคัญ**: อย่าลืมเปลี่ยน SECRET_KEY และรหัสผ่าน Admin ก่อน deploy production!

---

**เอกสารนี้จัดทำโดย**: R2R Development Team  
**อัพเดทล่าสุด**: February 2026  
**เวอร์ชัน**: 1.0

🚀 **ขอให้การ Deploy สำเร็จลุล่วง!**
