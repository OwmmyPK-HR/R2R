#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
init_db.py
สคริปต์สำหรับสร้างฐานข้อมูลและตารางทั้งหมดของระบบ R2R
รองรับทั้ง SQLite และ PostgreSQL
"""

import os
import sys

# เพิ่ม path ของโฟลเดอร์หลักเพื่อให้ import app ได้
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db

def init_database():
    """สร้างฐานข้อมูลและตารางทั้งหมด"""
    with app.app_context():
        try:
            print("=" * 60)
            print("กำลังเริ่มต้นระบบฐานข้อมูล R2R...")
            print("=" * 60)
            
            # แสดงข้อมูล database ที่จะสร้าง
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if db_uri.startswith('sqlite'):
                print(f"📁 ประเภทฐานข้อมูล: SQLite")
                db_path = db_uri.replace('sqlite:///', '')
                print(f"📁 ตำแหน่งไฟล์: {db_path}")
            else:
                print(f"📁 ประเภทฐานข้อมูล: PostgreSQL")
                # ซ่อน password ใน URL
                safe_uri = db_uri.split('@')[-1] if '@' in db_uri else db_uri
                print(f"📁 เชื่อมต่อกับ: {safe_uri}")
            
            print("\n🔧 กำลังสร้างตารางทั้งหมด...")
            
            # สร้างตารางทั้งหมดตาม models ใน app.py
            db.create_all()
            
            print("✅ สร้างตารางสำเร็จ!")
            print("\nตารางที่ถูกสร้าง:")
            print("  1. submission  - เก็บข้อมูลการยื่นคำขอ")
            print("  2. settings    - เก็บการตั้งค่าระบบ")
            
            # ตรวจสอบว่าตารางถูกสร้างแล้ว
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n📊 จำนวนตารางในฐานข้อมูล: {len(tables)}")
            
            # เพิ่มข้อมูล settings เริ่มต้น (ถ้ายังไม่มี)
            from app import Settings
            
            default_settings = [
                {
                    'key': 'page_charge_rate',
                    'value': '10000'
                },
                {
                    'key': 'int_journal_rate',
                    'value': '15000'
                },
                {
                    'key': 'int_journal_q1q2_rate',
                    'value': '20000'
                },
                {
                    'key': 'special_nat_rate',
                    'value': '12000'
                },
                {
                    'key': 'special_int_rate',
                    'value': '18000'
                },
                {
                    'key': 'creative_asean_rate',
                    'value': '15000'
                },
                {
                    'key': 'creative_inter_coop_rate',
                    'value': '12000'
                },
                {
                    'key': 'creative_national_rate',
                    'value': '10000'
                },
                {
                    'key': 'creative_institutional_rate',
                    'value': '8000'
                },
                {
                    'key': 'creative_public_rate',
                    'value': '5000'
                }
            ]
            
            print("\n🔧 กำลังตั้งค่าเริ่มต้น...")
            for setting in default_settings:
                existing = Settings.query.filter_by(key=setting['key']).first()
                if not existing:
                    new_setting = Settings(
                        key=setting['key'],
                        value=setting['value']
                    )
                    db.session.add(new_setting)
            
            db.session.commit()
            print("✅ ตั้งค่าเริ่มต้นสำเร็จ!")
            
            print("\n" + "=" * 60)
            print("🎉 สร้างฐานข้อมูลเสร็จสมบูรณ์!")
            print("=" * 60)
            print("\n💡 คุณสามารถเริ่มใช้งานระบบได้ทันที")
            print("   ใช้คำสั่ง: python app.py หรือ flask run")
            print()
            
            return True
            
        except Exception as e:
            print(f"\n❌ เกิดข้อผิดพลาด: {e}")
            print("กรุณาตรวจสอบการตั้งค่าฐานข้อมูลและลองใหม่อีกครั้ง")
            return False

def drop_all_tables():
    """ลบตารางทั้งหมด (ใช้เมื่อต้องการเริ่มต้นใหม่)"""
    with app.app_context():
        try:
            print("⚠️  คำเตือน: กำลังลบตารางทั้งหมด...")
            response = input("คุณแน่ใจหรือไม่? (yes/no): ")
            
            if response.lower() == 'yes':
                db.drop_all()
                print("✅ ลบตารางทั้งหมดเรียบร้อยแล้ว")
                return True
            else:
                print("ยกเลิกการลบตาราง")
                return False
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return False

def reset_database():
    """รีเซ็ตฐานข้อมูล - ลบและสร้างใหม่"""
    print("\n" + "=" * 60)
    print("🔄 รีเซ็ตฐานข้อมูล")
    print("=" * 60)
    
    if drop_all_tables():
        print("\n🔧 กำลังสร้างฐานข้อมูลใหม่...")
        return init_database()
    
    return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='จัดการฐานข้อมูล R2R System')
    parser.add_argument(
        '--reset',
        action='store_true',
        help='รีเซ็ตฐานข้อมูล (ลบและสร้างใหม่)'
    )
    
    args = parser.parse_args()
    
    if args.reset:
        reset_database()
    else:
        init_database()
