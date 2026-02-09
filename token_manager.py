#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
token_manager.py
ระบบจัดการ Token (API Token, JWT, Session) สำหรับ R2R System
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from app import db, Token, app
from flask import request


class TokenManager:
    """คลาสสำหรับจัดการ API tokens และ authentication"""
    
    @staticmethod
    def generate_token(length=32):
        """
        สร้าง token แบบสุ่ม
        
        Args:
            length (int): ความยาวของ token
        
        Returns:
            str: token ที่สร้างขึ้น
        """
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_token(token):
        """
        แฮช token สำหรับความปลอดภัย
        
        Args:
            token (str): token ที่ต้องการแฮช
        
        Returns:
            str: token ที่ถูกแฮช
        """
        return hashlib.sha256(token.encode()).hexdigest()
    
    @staticmethod
    def create_token(user_identifier, token_type='api', expires_in_days=30):
        """
        สร้าง token ใหม่
        
        Args:
            user_identifier (str): ชื่อหรือ ID ของผู้ใช้
            token_type (str): ประเภท token (api, jwt, session)
            expires_in_days (int): วันที่ token หมดอายุ
        
        Returns:
            Token: object token ที่สร้างขึ้น
        """
        try:
            # สร้าง token แบบสุ่ม
            raw_token = TokenManager.generate_token()
            
            # ตั้งค่าวันหมดอายุ
            expires_at = None
            if expires_in_days:
                expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
            
            # ดึง IP address และ User Agent
            ip_address = request.remote_addr if request else 'unknown'
            user_agent = request.headers.get('User-Agent') if request else 'unknown'
            
            # สร้าง token object
            token = Token(
                token=raw_token,
                user_identifier=user_identifier,
                expires_at=expires_at,
                ip_address=ip_address,
                user_agent=user_agent,
                token_type=token_type
            )
            
            with app.app_context():
                db.session.add(token)
                db.session.commit()
            
            print(f"✅ สร้าง {token_type} token สำหรับ {user_identifier}")
            
            return token
        
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการสร้าง token: {e}")
            return None
    
    @staticmethod
    def verify_token(token_string):
        """
        ตรวจสอบ token ว่าถูกต้องและยังใช้งานได้หรือไม่
        
        Args:
            token_string (str): token ที่ต้องการตรวจสอบ
        
        Returns:
            Token: object token ถ้าถูกต้อง หรือ None ถ้าไม่ถูกต้อง
        """
        try:
            token_obj = Token.query.filter_by(token=token_string).first()
            
            if not token_obj:
                return None
            
            # ตรวจสอบสถานะ
            if not token_obj.is_active:
                return None
            
            # ตรวจสอบการหมดอายุ
            if token_obj.is_expired():
                return None
            
            # อัพเดท last_used
            token_obj.last_used = datetime.utcnow()
            db.session.commit()
            
            return token_obj
        
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการตรวจสอบ token: {e}")
            return None
    
    @staticmethod
    def revoke_token(token_string):
        """
        ยกเลิก token (ทำให้ไม่สามารถใช้งานได้)
        
        Args:
            token_string (str): token ที่ต้องการยกเลิก
        
        Returns:
            bool: True ถ้าสำเร็จ, False ถ้าล้มเหลว
        """
        try:
            token_obj = Token.query.filter_by(token=token_string).first()
            
            if not token_obj:
                return False
            
            token_obj.is_active = False
            db.session.commit()
            
            print(f"✅ ยกเลิก token: {token_string[:20]}...")
            
            return True
        
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการยกเลิก token: {e}")
            return False
    
    @staticmethod
    def revoke_all_tokens(user_identifier):
        """
        ยกเลิกทุก token ของผู้ใช้
        
        Args:
            user_identifier (str): ชื่อหรือ ID ของผู้ใช้
        
        Returns:
            int: จำนวน token ที่ถูกยกเลิก
        """
        try:
            tokens = Token.query.filter_by(user_identifier=user_identifier, is_active=True).all()
            
            count = len(tokens)
            
            for token in tokens:
                token.is_active = False
            
            db.session.commit()
            
            print(f"✅ ยกเลิกทุก token ของ {user_identifier}: {count} tokens")
            
            return count
        
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการยกเลิก tokens: {e}")
            return 0
    
    @staticmethod
    def get_user_tokens(user_identifier, active_only=True):
        """
        ดึง tokens ของผู้ใช้
        
        Args:
            user_identifier (str): ชื่อหรือ ID ของผู้ใช้
            active_only (bool): ดึงเฉพาะ token ที่ยังใช้งานได้
        
        Returns:
            list: รายการ tokens
        """
        query = Token.query.filter_by(user_identifier=user_identifier)
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        return query.order_by(Token.created_at.desc()).all()
    
    @staticmethod
    def get_token_info(token_string):
        """
        ดึงข้อมูล token
        
        Args:
            token_string (str): token ที่ต้องการดูข้อมูล
        
        Returns:
            dict: ข้อมูล token
        """
        token_obj = Token.query.filter_by(token=token_string).first()
        
        if not token_obj:
            return None
        
        return token_obj.to_dict()
    
    @staticmethod
    def cleanup_expired_tokens():
        """
        ลบ tokens ที่หมดอายุ
        
        Returns:
            int: จำนวน token ที่ถูกลบ
        """
        try:
            now = datetime.utcnow()
            
            # ค้นหา tokens ที่หมดอายุ
            expired_tokens = Token.query.filter(
                Token.expires_at < now,
                Token.is_active == True
            ).all()
            
            count = len(expired_tokens)
            
            for token in expired_tokens:
                db.session.delete(token)
            
            db.session.commit()
            
            print(f"✅ ลบ tokens ที่หมดอายุ: {count} tokens")
            
            return count
        
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการลบ expired tokens: {e}")
            return 0
    
    @staticmethod
    def get_active_tokens_count(user_identifier=None):
        """
        นับจำนวน tokens ที่ยังใช้งานได้
        
        Args:
            user_identifier (str): ชื่อหรือ ID ของผู้ใช้ (ถ้ามี)
        
        Returns:
            int: จำนวน active tokens
        """
        query = Token.query.filter_by(is_active=True)
        
        if user_identifier:
            query = query.filter_by(user_identifier=user_identifier)
        
        return query.count()


# ตัวอย่างการใช้งาน:
# 
# # สร้าง token ใหม่
# token = TokenManager.create_token('admin', token_type='api', expires_in_days=30)
# print(f"Token: {token.token}")
#
# # ตรวจสอบ token
# verified = TokenManager.verify_token(token.token)
# if verified:
#     print(f"Token ถูกต้อง: {verified.user_identifier}")
#
# # ยกเลิก token
# TokenManager.revoke_token(token.token)
#
# # ดึง tokens ของผู้ใช้
# all_tokens = TokenManager.get_user_tokens('admin')
# for t in all_tokens:
#     print(f"Token: {t.token[:20]}... (expires: {t.expires_at})")
