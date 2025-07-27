import sqlite3
import os

def fix_database():
    """เพิ่มคอลัมน์ที่ขาดหายไปในฐานข้อมูล"""
    
    if not os.path.exists('database.db'):
        print("ไม่พบไฟล์ database.db")
        return
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        # ตรวจสอบคอลัมน์ที่มีอยู่
        cursor.execute("PRAGMA table_info(submission)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # เพิ่มคอลัมน์ที่ขาดหายไป
        missing_columns = [
            ('charge_int_q1q2_checkbox', 'BOOLEAN DEFAULT 0'),
            ('charge_int_q1q2_amount', 'VARCHAR(50)')
        ]
        
        for col_name, col_type in missing_columns:
            if col_name not in columns:
                cursor.execute(f"ALTER TABLE submission ADD COLUMN {col_name} {col_type}")
                print(f"เพิ่มคอลัมน์ {col_name} สำเร็จ")
            else:
                print(f"คอลัมน์ {col_name} มีอยู่แล้ว")
        
        conn.commit()
        print("แก้ไขฐานข้อมูลเสร็จสิ้น")
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    fix_database()