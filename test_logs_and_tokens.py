#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_logs_and_tokens.py
สคริปต์สำหรับทดสอบระบบ Logging และ Token Management
"""

import os
import sys
from datetime import datetime, timedelta

# เพิ่ม path เพื่อให้สามารถ import app ได้
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Log, Token


def test_logging():
    """ทดสอบระบบ Logging"""
    print("\n" + "=" * 60)
    print("🧪 ทดสอบระบบ Logging")
    print("=" * 60)
    
    from logging_utils import SystemLogger
    
    # ทดสอบ 1: บันทึก INFO
    print("\n✓ ทดสอบ 1: บันทึก INFO level")
    with app.app_context():
        SystemLogger.info("นี่คือข้อความ INFO ทดสอบ", action="test")
        log = Log.query.order_by(Log.id.desc()).first()
        if log and log.level == "INFO":
            print(f"✅ สำเร็จ: {log.message}")
        else:
            print("❌ ล้มเหลว")
    
    # ทดสอบ 2: บันทึก ERROR
    print("\n✓ ทดสอบ 2: บันทึก ERROR level")
    with app.app_context():
        SystemLogger.error("นี่คือข้อความ ERROR ทดสอบ", action="test")
        log = Log.query.filter_by(level="ERROR").order_by(Log.id.desc()).first()
        if log:
            print(f"✅ สำเร็จ: {log.message}")
        else:
            print("❌ ล้มเหลว")
    
    # ทดสอบ 3: บันทึก submission
    print("\n✓ ทดสอบ 3: บันทึกการยื่นคำขอ")
    with app.app_context():
        SystemLogger.log_submission("create", submission_id=999, details="ทดสอบ")
        log = Log.query.filter_by(submission_id=999).first()
        if log:
            print(f"✅ สำเร็จ: {log.message}")
        else:
            print("❌ ล้มเหลว")
    
    # ทดสอบ 4: ดึง logs
    print("\n✓ ทดสอบ 4: ดึงข้อมูล logs")
    with app.app_context():
        logs = SystemLogger.get_logs(limit=5)
        if logs:
            print(f"✅ สำเร็จ: ได้ logs {len(logs)} รายการ")
            for log in logs:
                print(f"   - {log.level}: {log.message}")
        else:
            print("❌ ล้มเหลว: ไม่มี logs")
    
    # ทดสอบ 5: กรองตามระดับ
    print("\n✓ ทดสอบ 5: กรองตามระดับ ERROR")
    with app.app_context():
        error_logs = SystemLogger.get_logs(level="ERROR")
        if error_logs:
            print(f"✅ สำเร็จ: ได้ ERROR logs {len(error_logs)} รายการ")
        else:
            print("⚠️  ไม่มี ERROR logs")


def test_tokens():
    """ทดสอบระบบ Token Management"""
    print("\n" + "=" * 60)
    print("🧪 ทดสอบระบบ Token Management")
    print("=" * 60)
    
    from token_manager import TokenManager
    
    # ทดสอบ 1: สร้าง token
    print("\n✓ ทดสอบ 1: สร้าง token ใหม่")
    with app.app_context():
        token = TokenManager.create_token(
            'test_user',
            token_type='api',
            expires_in_days=7
        )
        if token:
            print(f"✅ สำเร็จ: สร้าง token")
            print(f"   Token: {token.token[:30]}...")
            print(f"   User: {token.user_identifier}")
            print(f"   Type: {token.token_type}")
            test_token_string = token.token
        else:
            print("❌ ล้มเหลว")
            return
    
    # ทดสอบ 2: ตรวจสอบ token
    print("\n✓ ทดสอบ 2: ตรวจสอบ token")
    with app.app_context():
        verified = TokenManager.verify_token(test_token_string)
        if verified:
            print(f"✅ สำเร็จ: Token ถูกต้อง")
            print(f"   User: {verified.user_identifier}")
            print(f"   Last used: {verified.last_used}")
        else:
            print("❌ ล้มเหลว: Token ไม่ถูกต้อง")
    
    # ทดสอบ 3: ตรวจสอบ token ไม่ถูกต้อง
    print("\n✓ ทดสอบ 3: ตรวจสอบ token ที่ไม่ถูกต้อง")
    with app.app_context():
        invalid = TokenManager.verify_token("invalid_token_12345")
        if not invalid:
            print(f"✅ สำเร็จ: ระบบตรวจสอบได้ว่า token ไม่ถูกต้อง")
        else:
            print("❌ ล้มเหลว")
    
    # ทดสอบ 4: ดึง tokens ของผู้ใช้
    print("\n✓ ทดสอบ 4: ดึง tokens ของผู้ใช้")
    with app.app_context():
        tokens = TokenManager.get_user_tokens('test_user')
        if tokens:
            print(f"✅ สำเร็จ: ได้ tokens {len(tokens)} รายการ")
            for t in tokens:
                print(f"   - Created: {t.created_at}")
        else:
            print("⚠️  ไม่มี tokens ของผู้ใช้นี้")
    
    # ทดสอบ 5: นับ active tokens
    print("\n✓ ทดสอบ 5: นับ active tokens")
    with app.app_context():
        count = TokenManager.get_active_tokens_count()
        print(f"✅ Active tokens ทั้งหมด: {count}")
    
    # ทดสอบ 6: ยกเลิก token
    print("\n✓ ทดสอบ 6: ยกเลิก token")
    with app.app_context():
        success = TokenManager.revoke_token(test_token_string)
        if success:
            print(f"✅ สำเร็จ: ยกเลิก token")
            # ตรวจสอบว่า token ถูกยกเลิก
            verified = TokenManager.verify_token(test_token_string)
            if not verified:
                print(f"✅ ยืนยัน: Token ไม่สามารถใช้งานได้แล้ว")
            else:
                print("❌ Error: Token ยังสามารถใช้งานได้")
        else:
            print("❌ ล้มเหลว")


def test_database_integration():
    """ทดสอบการบูรณาการกับฐานข้อมูล"""
    print("\n" + "=" * 60)
    print("🧪 ทดสอบการบูรณาการกับฐานข้อมูล")
    print("=" * 60)
    
    with app.app_context():
        # ทดสอบ 1: ตรวจสอบตาราง
        print("\n✓ ทดสอบ 1: ตรวจสอบตาราง logs")
        try:
            log_count = Log.query.count()
            print(f"✅ สำเร็จ: จำนวน logs = {log_count}")
        except Exception as e:
            print(f"❌ ล้มเหลว: {e}")
        
        # ทดสอบ 2: ตรวจสอบตาราง tokens
        print("\n✓ ทดสอบ 2: ตรวจสอบตาราง tokens")
        try:
            token_count = Token.query.count()
            print(f"✅ สำเร็จ: จำนวน tokens = {token_count}")
        except Exception as e:
            print(f"❌ ล้มเหลว: {e}")
        
        # ทดสอบ 3: ตรวจสอบ constraints
        print("\n✓ ทดสอบ 3: ตรวจสอบ unique constraint")
        from token_manager import TokenManager
        token1 = TokenManager.create_token('unique_test', token_type='api')
        try:
            # พยายามสร้าง token เดียวกัน (ควรล้มเหลว)
            db.session.execute(
                'INSERT INTO tokens (token, user_identifier, token_type) VALUES (?, ?, ?)',
                (token1.token, 'another_user', 'api')
            )
            db.session.commit()
            print("❌ ล้มเหลว: Unique constraint ไม่ทำงาน")
        except Exception as e:
            print("✅ สำเร็จ: Unique constraint ทำงานถูกต้อง")


def print_statistics():
    """พิมพ์สถิติการใช้งาน"""
    print("\n" + "=" * 60)
    print("📊 สถิติการใช้งาน")
    print("=" * 60)
    
    with app.app_context():
        # สถิติ Logs
        print("\n📝 บันทึก (Logs)")
        total_logs = Log.query.count()
        info_logs = Log.query.filter_by(level="INFO").count()
        error_logs = Log.query.filter_by(level="ERROR").count()
        warning_logs = Log.query.filter_by(level="WARNING").count()
        
        print(f"  ทั้งหมด: {total_logs}")
        print(f"  - INFO: {info_logs}")
        print(f"  - ERROR: {error_logs}")
        print(f"  - WARNING: {warning_logs}")
        
        # สถิติ Tokens
        print("\n🔑 Token")
        total_tokens = Token.query.count()
        active_tokens = Token.query.filter_by(is_active=True).count()
        inactive_tokens = total_tokens - active_tokens
        
        print(f"  ทั้งหมด: {total_tokens}")
        print(f"  - ใช้งานได้: {active_tokens}")
        print(f"  - ไม่ใช้งาน: {inactive_tokens}")
        
        # Active tokens โดยผู้ใช้
        users = db.session.query(Token.user_identifier).distinct().all()
        if users:
            print(f"\n  Tokens โดยผู้ใช้:")
            for user in users:
                count = Token.query.filter_by(
                    user_identifier=user[0],
                    is_active=True
                ).count()
                print(f"  - {user[0]}: {count}")


def main():
    """เรียกใช้ทุกการทดสอบ"""
    print("\n🚀 เริ่มการทดสอบระบบ Logging และ Token Management")
    print("=" * 60)
    
    try:
        # สร้างตารางถ้ายังไม่มี
        with app.app_context():
            db.create_all()
            print("✅ ตารางฐานข้อมูลพร้อมใช้งาน")
        
        # เรียกใช้การทดสอบ
        test_logging()
        test_tokens()
        test_database_integration()
        print_statistics()
        
        print("\n" + "=" * 60)
        print("✅ ทดสอบเสร็จสิ้น!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
