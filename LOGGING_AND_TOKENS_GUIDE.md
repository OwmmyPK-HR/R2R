# 📝 ระบบบันทึก (Logging) และ Token Management

ระบบ R2R มีระบบจัดการบันทึกและ token ที่รองรับการติดตามการทำงานของระบบและการยืนยันตัวตน

---

## 🗄️ ตารางฐานข้อมูล

### 1. ตาราง `logs` - บันทึกการทำงาน

| ฟิลด์ | ประเภท | คำอธิบาย |
|------|--------|---------|
| `id` | Integer | รหัสบันทึก (Primary Key) |
| `timestamp` | DateTime | วันเวลาที่บันทึก |
| `level` | String | ระดับของบันทึก (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `message` | Text | ข้อความบันทึก |
| `user_id` | String | รหัส/ชื่อผู้ใช้ |
| `ip_address` | String | ที่อยู่ IP ของผู้ใช้ |
| `action` | String | การกระทำที่ทำ (create, read, update, delete) |
| `submission_id` | Integer | ID ของคำขอที่เกี่ยวข้อง |
| `details` | Text | รายละเอียดเพิ่มเติม |

### 2. ตาราง `tokens` - การจัดการ Token

| ฟิลด์ | ประเภท | คำอธิบาย |
|------|--------|---------|
| `id` | Integer | รหัส Token (Primary Key) |
| `token` | String | Token ที่สร้างขึ้น (Unique) |
| `user_identifier` | String | ชื่อหรือรหัสผู้ใช้ |
| `created_at` | DateTime | วันเวลาที่สร้าง |
| `expires_at` | DateTime | วันเวลาที่หมดอายุ |
| `is_active` | Boolean | สถานะ (ใช้งานได้หรือไม่) |
| `last_used` | DateTime | ใช้ล่าสุดเมื่อไร |
| `ip_address` | String | IP ที่สร้าง Token |
| `user_agent` | String | Browser/Client ที่ใช้ |
| `token_type` | String | ประเภท Token (api, jwt, session) |

---

## 📜 วิธีใช้งาน

### 1. ใช้งานระบบ Logging

#### นำเข้า logger
```python
from logging_utils import SystemLogger
```

#### บันทึกข้อมูล
```python
# บันทึก INFO level
SystemLogger.info("ข้อความบันทึก", action="create", submission_id=1)

# บันทึก ERROR level
SystemLogger.error("เกิดข้อผิดพลาด", action="update", submission_id=1)

# บันทึกการยื่นคำขอ
SystemLogger.log_submission("create", submission_id=5, details="ยื่นคำขอใหม่เรียบร้อย")

# บันทึกการอัพโหลดไฟล์
SystemLogger.log_file_upload("document.pdf", submission_id=1, success=True)

# บันทึกการล็อกอิน
SystemLogger.log_login("admin", success=True)
```

#### ดึงข้อมูล Logs
```python
# ดึง 100 รายการล่าสุด
logs = SystemLogger.get_logs(limit=100)

# ดึง logs ตามระดับ
logs = SystemLogger.get_logs(level="ERROR")

# ดึง logs ตามผู้ใช้
logs = SystemLogger.get_logs(user_id="admin")

# ดึง logs ของ submission
logs = SystemLogger.get_logs_by_submission(submission_id=1)
for log in logs:
    print(f"{log.level}: {log.message}")

# ลบ logs เก่ากว่า 30 วัน
deleted_count = SystemLogger.clear_old_logs(days=30)
```

### 2. ใช้งาน Token Management

#### นำเข้า token manager
```python
from token_manager import TokenManager
```

#### สร้าง Token ใหม่
```python
# สร้าง API token ที่มีอายุ 30 วัน
token = TokenManager.create_token('admin', token_type='api', expires_in_days=30)
print(f"Token Hash (stored): {token.token}")

# ค่า raw token ใช้แสดง/ส่งต่อให้ผู้ใช้ครั้งเดียว (ไม่ได้ถูกเก็บใน DB)
print(f"Token Raw (one-time): {token._raw_token}")

# สร้าง token ที่ไม่มีอายุ (indefinite)
token = TokenManager.create_token('system', token_type='jwt', expires_in_days=None)
```

#### ตรวจสอบ Token
```python
# ตรวจสอบว่า token ถูกต้อง
# หมายเหตุ: verify_token ในโค้ดปัจจุบันใช้ค่าที่เก็บในคอลัมน์ token โดยตรง
# (ปัจจุบันคือค่า hash)
token_obj = TokenManager.verify_token('stored-token-hash')
if token_obj:
    print(f"✅ Token ถูกต้อง สำหรับ {token_obj.user_identifier}")
else:
    print("❌ Token ไม่ถูกต้อง หรือหมดอายุแล้ว")
```

#### ยกเลิก Token
```python
# ยกเลิก token เดียว
TokenManager.revoke_token('your-token-here')

# ยกเลิกทุก token ของผู้ใช้
TokenManager.revoke_all_tokens('admin')
```

#### ดูข้อมูล Token
```python
# ดึง tokens ของผู้ใช้
tokens = TokenManager.get_user_tokens('admin', active_only=True)
for token in tokens:
    print(f"Token: {token.token[:20]}...")
    print(f"Expires: {token.expires_at}")

# ดึงข้อมูล token เดียว
info = TokenManager.get_token_info('your-token-here')
print(info)

# นับ active tokens
count = TokenManager.get_active_tokens_count()
print(f"Active tokens: {count}")

# ลบ tokens ที่หมดอายุ
deleted = TokenManager.cleanup_expired_tokens()
print(f"Deleted {deleted} expired tokens")
```

---

## 🔌 API Endpoints

> ทุก endpoint ด้านล่างต้องเป็น **admin session** (`admin_logged_in`) และมี **rate limit**
> โดย endpoint ที่เปลี่ยนข้อมูล (`DELETE`, `POST`) ต้องส่ง **CSRF token** ด้วย

### Logs Endpoints

#### ดึง logs
```
GET /api/logs
GET /api/logs?limit=50&level=ERROR&user_id=admin
```

ตัวอย่าง Response:
```json
[
  {
    "id": 1,
    "timestamp": "2025-02-09T10:30:00",
    "level": "INFO",
    "message": "ยื่นคำขอสำเร็จ",
    "user_id": "admin",
    "ip_address": "192.168.1.100",
    "action": "create",
    "submission_id": 1,
    "details": "ยื่นคำขอใหม่เรียบร้อย"
  }
]
```

#### ดึง logs ของ submission
```
GET /api/logs/submission/1
```

### Tokens Endpoints

#### ดึง tokens ทั้งหมด
```
GET /api/tokens
```

ตัวอย่าง Response:
```json
[
  {
    "id": 1,
    "token": "abc123...",
    "user_identifier": "admin",
    "created_at": "2025-02-09T10:00:00",
    "expires_at": "2025-03-11T10:00:00",
    "is_active": true,
    "last_used": "2025-02-09T15:30:00",
    "token_type": "api"
  }
]
```

#### ยกเลิก token
```
DELETE /api/tokens/1
```

#### ลบ tokens ที่หมดอายุ
```
POST /api/tokens/cleanup
```

### Rate Limits (ตามโค้ดปัจจุบัน)

- `GET /api/logs` -> `60 per minute`
- `GET /api/logs/submission/<id>` -> `60 per minute`
- `GET /api/tokens` -> `30 per minute`
- `DELETE /api/tokens/<id>` -> `20 per minute`
- `POST /api/tokens/cleanup` -> `5 per minute`

---

## 🎯 ตัวอย่างการใช้งานจริง

### ตัวอย่าง 1: บันทึกการยื่นคำขอใหม่

```python
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # ประมวลผลการยื่นคำขอ...
        submission = Submission()
        # ... อื่นๆ ...
        db.session.add(submission)
        db.session.commit()
        
        # บันทึก
        SystemLogger.log_submission(
            'create', 
            submission_id=submission.id,
            details=f"ยื่นคำขอจาก {submission.full_name}"
        )
        
        return jsonify({'status': 'success'})
    except Exception as e:
        SystemLogger.error(
            f"การยื่นคำขอล้มเหลว: {e}",
            action='create'
        )
        return jsonify({'status': 'error'}), 500
```

### ตัวอย่าง 2: ตรวจสอบ Token ก่อนดำเนินการ

```python
@app.route('/api/protected', methods=['GET'])
def protected_route():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    token_obj = TokenManager.verify_token(token)
    if not token_obj:
        SystemLogger.warning(
            "ความพยายามเข้าถึงด้วย token ที่ไม่ถูกต้อง",
            action="auth"
        )
        return jsonify({'error': 'Invalid token'}), 401
    
    # ทำการประมวลผลที่หมายตัวอักษร...
    return jsonify({'data': 'secret data'})
```

### ตัวอย่าง 3: สร้าง Admin API Token

```python
# เมื่อสร้าง admin user ครั้งแรก
from token_manager import TokenManager

admin_token = TokenManager.create_token(
    user_identifier='admin',
    token_type='api',
    expires_in_days=365  # Token มีอายุ 1 ปี
)

print(f"Admin API Token Hash: {admin_token.token}")
print(f"Admin API Token Raw (one-time): {admin_token._raw_token}")
print("บันทึก raw token นี้ไว้ในที่ปลอดภัย เพราะระบบไม่เก็บ plaintext")
```

---

## 📊 การจัดการประเมินผล

### ดู Logs ใน Admin Panel

Admin สามารถเข้าดูข้อมูล logs จาก Admin Dashboard:
- จำนวน logs ตามระดับ (INFO, WARNING, ERROR)
- กิจกรรมผู้ใช้
- การเปลี่ยนแปลงข้อมูล
- ข้อผิดพลาดของระบบ

### ตรวจสอบ Tokens ที่ใช้งาน

Admin สามารถดูและจัดการ tokens:
- ยกเลิก tokens ที่ไม่ใช้
- ลบ tokens ที่หมดอายุ
- ดูประวัติการใช้งาน token

---

## ⚙️ การปรับแต่ง

### การตั้งค่า Log Levels

```python
# ตั้งค่าให้บันทึกเฉพาะ ERROR ขึ้นไป
# ในส่วนของระบบการบันทึก (logging.py)
```

### การตั้งค่า Token Expiration

```python
# ตั้งค่าเวลา expiration เมื่อสร้าง token
token = TokenManager.create_token(
    'user',
    token_type='api',
    expires_in_days=90  # เปลี่ยนจำนวนวันตามต้องการ
)
```

---

## 🔒 ความปลอดภัย

### สิ่งที่ต้องหมั่นไส

1. **ไม่ให้ token ไม่มีอายุ** - ควรมีวันหมดอายุเสมอ
2. **ลบ logs เก่า** - ใช้ `SystemLogger.clear_old_logs()` อย่างสม่ำเสมอ
3. **บันทึกการเข้าถึง** - ล็อคลิสต์ของใครเข้าถึง API
4. **หมุนเวียน tokens** - เปลี่ยน tokens เก่าเป็นใหม่เป็นระยะๆ
5. **ตรวจสอบ logs** - ระบบตรวจสอบ logs เป็นประจำเพื่อหาความผิดปกติ
6. **ป้องกัน CSRF สำหรับ API ที่เปลี่ยนข้อมูล** - ต้องส่ง CSRF token กับ `DELETE/POST` เสมอ

---

## 📋 Maintenance Tasks

### ทำความสะอาด logs
```bash
python -c "from logging_utils import SystemLogger; SystemLogger.clear_old_logs(30)"
```

### ลบ expired tokens
```bash
python -c "from token_manager import TokenManager; TokenManager.cleanup_expired_tokens()"
```

### ตรวจสอบสถานะ
```bash
python -c "
from token_manager import TokenManager
count = TokenManager.get_active_tokens_count()
print(f'Active Tokens: {count}')
"
```

---

หากมีคำถามเพิ่มเติมหรือต้องการความช่วยเหลือ โปรดติดต่อผู้ดูแลระบบ
