# migrate_add_q1q2_fields.py
# สคริปต์สำหรับเพิ่มฟิลด์ charge_int_q1q2_checkbox และ charge_int_q1q2_amount ลงในฐานข้อมูลที่มีอยู่แล้ว

import os
import sqlite3
from sqlalchemy import text
from app import app, db

def add_q1q2_fields():
    """เพิ่มฟิลด์ Q1 Q2 ลงในตาราง submission หากยังไม่มี"""
    
    with app.app_context():
        try:
            # ตรวจสอบว่าใช้ SQLite หรือ PostgreSQL
            database_url = app.config['SQLALCHEMY_DATABASE_URI']
            
            if database_url.startswith('sqlite'):
                # สำหรับ SQLite
                # ตรวจสอบว่าฟิลด์มีอยู่แล้วหรือไม่
                result = db.session.execute(text("PRAGMA table_info(submission)")).fetchall()
                columns = [row[1] for row in result]  # row[1] คือชื่อคอลัมน์
                
                if 'charge_int_q1q2_checkbox' not in columns:
                    print("เพิ่มฟิลด์ charge_int_q1q2_checkbox ลงในตาราง submission...")
                    db.session.execute(text("ALTER TABLE submission ADD COLUMN charge_int_q1q2_checkbox BOOLEAN DEFAULT 0"))
                    db.session.commit()
                    print("เพิ่มฟิลด์ charge_int_q1q2_checkbox สำเร็จ!")
                else:
                    print("ฟิลด์ charge_int_q1q2_checkbox มีอยู่แล้ว")
                
                if 'charge_int_q1q2_amount' not in columns:
                    print("เพิ่มฟิลด์ charge_int_q1q2_amount ลงในตาราง submission...")
                    db.session.execute(text("ALTER TABLE submission ADD COLUMN charge_int_q1q2_amount VARCHAR(50)"))
                    db.session.commit()
                    print("เพิ่มฟิลด์ charge_int_q1q2_amount สำเร็จ!")
                else:
                    print("ฟิลด์ charge_int_q1q2_amount มีอยู่แล้ว")
                    
            else:
                # สำหรับ PostgreSQL
                # ตรวจสอบฟิลด์ checkbox
                result = db.session.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='submission' AND column_name='charge_int_q1q2_checkbox'
                """)).fetchall()
                
                if not result:
                    print("เพิ่มฟิลด์ charge_int_q1q2_checkbox ลงในตาราง submission...")
                    db.session.execute(text("ALTER TABLE submission ADD COLUMN charge_int_q1q2_checkbox BOOLEAN DEFAULT FALSE"))
                    db.session.commit()
                    print("เพิ่มฟิลด์ charge_int_q1q2_checkbox สำเร็จ!")
                else:
                    print("ฟิลด์ charge_int_q1q2_checkbox มีอยู่แล้ว")
                
                # ตรวจสอบฟิลด์ amount
                result = db.session.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='submission' AND column_name='charge_int_q1q2_amount'
                """)).fetchall()
                
                if not result:
                    print("เพิ่มฟิลด์ charge_int_q1q2_amount ลงในตาราง submission...")
                    db.session.execute(text("ALTER TABLE submission ADD COLUMN charge_int_q1q2_amount VARCHAR(50)"))
                    db.session.commit()
                    print("เพิ่มฟิลด์ charge_int_q1q2_amount สำเร็จ!")
                else:
                    print("ฟิลด์ charge_int_q1q2_amount มีอยู่แล้ว")
                    
        except Exception as e:
            db.session.rollback()
            print(f"เกิดข้อผิดพลาดในการเพิ่มฟิลด์: {e}")
            return False
        
        return True

if __name__ == '__main__':
    print("เริ่มต้นการ migrate ฐานข้อมูล...")
    if add_q1q2_fields():
        print("Migration สำเร็จ!")
    else:
        print("Migration ล้มเหลว!")