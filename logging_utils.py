#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
logging_utils.py
ระบบบันทึก (Logging) สำหรับ R2R System
บันทึกการกระทำและเหตุการณ์สำคัญของระบบ
"""

from datetime import datetime
from flask import request
from app import db, Log, app


class SystemLogger:
    """คลาสสำหรับบันทึกข้อมูลการทำงานของระบบ"""
    
    @staticmethod
    def get_user_id():
        """ดึงรหัสผู้ใช้จาก session"""
        from flask import session
        return session.get('user_id', 'anonymous')
    
    @staticmethod
    def get_ip_address():
        """ดึง IP address ของผู้ใช้"""
        if request:
            return request.remote_addr or 'unknown'
        return 'unknown'
    
    @staticmethod
    def get_user_agent():
        """ดึง User Agent"""
        if request:
            return request.headers.get('User-Agent', 'unknown')
        return 'unknown'
    
    @staticmethod
    def log(level, message, action=None, submission_id=None, details=None):
        """
        บันทึกข้อมูลลงฐานข้อมูล
        
        Args:
            level (str): ระดับ log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message (str): ข้อความที่ต้องการบันทึก
            action (str): การกระทำที่ทำ (create, read, update, delete)
            submission_id (int): ID ของการยื่นคำขอ (ถ้ามี)
            details (str): รายละเอียดเพิ่มเติม
        """
        try:
            log_entry = Log(
                level=level.upper(),
                message=message,
                user_id=SystemLogger.get_user_id(),
                ip_address=SystemLogger.get_ip_address(),
                action=action,
                submission_id=submission_id,
                details=details
            )
            
            with app.app_context():
                db.session.add(log_entry)
                db.session.commit()
                
            # พิมพ์ลงหน้าจอด้วย
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] [{level.upper()}] {message}")
            
            return log_entry
            
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการบันทึก log: {e}")
            return None
    
    @staticmethod
    def info(message, action=None, submission_id=None, details=None):
        """บันทึก INFO level"""
        return SystemLogger.log('INFO', message, action, submission_id, details)
    
    @staticmethod
    def debug(message, action=None, submission_id=None, details=None):
        """บันทึก DEBUG level"""
        return SystemLogger.log('DEBUG', message, action, submission_id, details)
    
    @staticmethod
    def warning(message, action=None, submission_id=None, details=None):
        """บันทึก WARNING level"""
        return SystemLogger.log('WARNING', message, action, submission_id, details)
    
    @staticmethod
    def error(message, action=None, submission_id=None, details=None):
        """บันทึก ERROR level"""
        return SystemLogger.log('ERROR', message, action, submission_id, details)
    
    @staticmethod
    def critical(message, action=None, submission_id=None, details=None):
        """บันทึก CRITICAL level"""
        return SystemLogger.log('CRITICAL', message, action, submission_id, details)
    
    @staticmethod
    def log_submission(action, submission_id, details=None):
        """บันทึกการทำงานกับ submission"""
        message = f"ยื่นคำขอ ID {submission_id}: {action}"
        SystemLogger.log('INFO', message, action=action, submission_id=submission_id, details=details)
    
    @staticmethod
    def log_file_upload(filename, submission_id, success=True):
        """บันทึกการอัพโหลดไฟล์"""
        action = 'upload'
        message = f"{'✅ อัพโหลด' if success else '❌ อัพโหลดล้มเหลว'} ไฟล์: {filename}"
        level = 'INFO' if success else 'ERROR'
        SystemLogger.log(level, message, action=action, submission_id=submission_id)
    
    @staticmethod
    def log_login(user_id, success=True):
        """บันทึกการล็อกอิน"""
        message = f"{'✅ ล็อกอิน' if success else '❌ ล็อกอินล้มเหลว'}: {user_id}"
        level = 'INFO' if success else 'WARNING'
        SystemLogger.log(level, message, action='login')
    
    @staticmethod
    def get_logs(limit=100, level=None, user_id=None):
        """
        ดึงข้อมูล logs
        
        Args:
            limit (int): จำนวนข้อมูลสูงสุด
            level (str): กรองตามระดับ (ถ้ามี)
            user_id (str): กรองตามผู้ใช้ (ถ้ามี)
        
        Returns:
            list: รายการ logs
        """
        query = Log.query
        
        if level:
            query = query.filter_by(level=level.upper())
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        return query.order_by(Log.timestamp.desc()).limit(limit).all()
    
    @staticmethod
    def get_logs_by_submission(submission_id):
        """ดึง logs ที่เกี่ยวข้องกับ submission"""
        return Log.query.filter_by(submission_id=submission_id).order_by(Log.timestamp.desc()).all()
    
    @staticmethod
    def clear_old_logs(days=30):
        """ลบ logs เก่าที่เกิน X วัน"""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        deleted = Log.query.filter(Log.timestamp < cutoff_date).delete()
        db.session.commit()
        
        message = f"ลบ logs เก่ากว่า {days} วัน: {deleted} รายการ"
        SystemLogger.info(message)
        
        return deleted


# ตัวอย่างการใช้งาน:
# SystemLogger.info("ระบบเริ่มทำงาน")
# SystemLogger.log_submission('create', submission_id=1, details="ยื่นคำขอใหม่")
# SystemLogger.log_file_upload('document.pdf', submission_id=1)
# SystemLogger.log_login('admin', success=True)
