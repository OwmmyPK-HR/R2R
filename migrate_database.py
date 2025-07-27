# migrate_database.py
# สคริปต์สำหรับเพิ่มฟิลด์ scope_2_3 ลงในฐานข้อมูลที่มีอยู่แล้ว

import os
import sqlite3
from sqlalchemy import text
from app import app, db

def add_scope_2_3_field():
    """เพิ่มฟิลด์ scope_2_3 ลงในตาราง submission หากยังไม่มี"""
    
    with app.app_context():
        try:
            # ตรวจสอบว่าใช้ SQLite หรือ PostgreSQL
            database_url = app.config['SQLALCHEMY_DATABASE_URI']
            
            if database_url.startswith('sqlite'):
                # สำหรับ SQLite
                # ตรวจสอบว่าฟิลด์มีอยู่แล้วหรือไม่
                result = db.session.execute(text("PRAGMA table_info(submission)")).fetchall()
                columns = [row[1] for row in result]  # row[1] คือชื่อคอลัมน์
                
                if 'scope_2_3' not in columns:
                    print("เพิ่มฟิลด์ scope_2_3 ลงในตาราง submission...")
                    db.session.execute(text("ALTER TABLE submission ADD COLUMN scope_2_3 BOOLEAN DEFAULT 0"))
                    db.session.commit()
                    print("เพิ่มฟิลด์ scope_2_3 สำเร็จ!")
                else:
                    print("ฟิลด์ scope_2_3 มีอยู่แล้ว")
                    
            else:
                # สำหรับ PostgreSQL
                # ตรวจสอบว่าฟิลด์มีอยู่แล้วหรือไม่
                result = db.session.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='submission' AND column_name='scope_2_3'
                """)).fetchall()
                
                if not result:
                    print("เพิ่มฟิลด์ scope_2_3 ลงในตาราง submission...")
                    db.session.execute(text("ALTER TABLE submission ADD COLUMN scope_2_3 BOOLEAN DEFAULT FALSE"))
                    db.session.commit()
                    print("เพิ่มฟิลด์ scope_2_3 สำเร็จ!")
                else:
                    print("ฟิลด์ scope_2_3 มีอยู่แล้ว")
                    
        except Exception as e:
            db.session.rollback()
            print(f"เกิดข้อผิดพลาดในการเพิ่มฟิลด์: {e}")
            return False
        
        return True

if __name__ == '__main__':
    print("เริ่มต้นการ migrate ฐานข้อมูล...")
    if add_scope_2_3_field():
        print("Migration สำเร็จ!")
    else:
        print("Migration ล้มเหลว!")
