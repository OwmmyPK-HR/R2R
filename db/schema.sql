-- ========================================
-- R2R System Database Schema (SQLite)
-- ระบบคำขอค่าตอบแทนผลงานตีพิมพ์
-- ========================================

-- ตาราง submission: เก็บข้อมูลการส่งคำขอทั้งหมด
CREATE TABLE IF NOT EXISTS submission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    consent_evidence_pdf VARCHAR(300),
    
    -- Part 1: ข้อมูลผู้ยื่นคำขอ
    full_name VARCHAR(200),
    academic_position VARCHAR(200),
    affiliation VARCHAR(200),
    phone VARCHAR(50),
    mobile_phone VARCHAR(50),
    email VARCHAR(100),
    
    -- Part 2: ข้อมูลผลงาน
    work_name_th VARCHAR(300),
    work_name_en VARCHAR(300),
    funding_source VARCHAR(200),
    fiscal_year VARCHAR(20),
    project_name VARCHAR(300),
    qual_1_1 BOOLEAN DEFAULT 0,
    qual_1_2 BOOLEAN DEFAULT 0,
    qual_1_3 BOOLEAN DEFAULT 0,
    scope_2_1 BOOLEAN DEFAULT 0,
    scope_2_2 BOOLEAN DEFAULT 0,
    scope_2_3 BOOLEAN DEFAULT 0,
    payment_3_1 BOOLEAN DEFAULT 0,
    page_charge_amount VARCHAR(50),
    payment_3_2 BOOLEAN DEFAULT 0,
    payment_3_3 BOOLEAN DEFAULT 0,
    num_institutes_3_3 VARCHAR(50),
    share_amount_3_3 VARCHAR(50),
    
    -- Part 4: ค่าตอบแทนวารสารระดับนานาชาติ
    charge_int_checkbox BOOLEAN DEFAULT 0,
    charge_int_amount VARCHAR(50),
    charge_int_q1q2_checkbox BOOLEAN DEFAULT 0,
    charge_int_q1q2_amount VARCHAR(50),
    remuneration_int_checkbox BOOLEAN DEFAULT 0,
    international_quartile VARCHAR(50),
    share_int_checkbox BOOLEAN DEFAULT 0,
    share_int_base_amount VARCHAR(50),
    share_int_num_institutes VARCHAR(50),
    share_int_final_amount VARCHAR(50),
    
    -- Part 5: วารสารพิเศษ
    special_nat_checkbox BOOLEAN DEFAULT 0,
    special_nat_share_checkbox BOOLEAN DEFAULT 0,
    special_nat_share_num_institutes VARCHAR(50),
    special_nat_share_final_amount VARCHAR(50),
    special_int_checkbox BOOLEAN DEFAULT 0,
    special_international_quartile VARCHAR(50),
    special_int_share_checkbox BOOLEAN DEFAULT 0,
    special_int_share_base_amount VARCHAR(50),
    special_int_share_num_institutes VARCHAR(50),
    special_int_share_final_amount VARCHAR(50),
    
    -- Part 6: ผลงานสร้างสรรค์
    creative_level_asean BOOLEAN DEFAULT 0,
    creative_level_inter_coop BOOLEAN DEFAULT 0,
    creative_level_national BOOLEAN DEFAULT 0,
    creative_level_institutional BOOLEAN DEFAULT 0,
    creative_level_public BOOLEAN DEFAULT 0,
    creative_share_checkbox BOOLEAN DEFAULT 0,
    creative_share_base_amount VARCHAR(50),
    creative_share_num_institutes VARCHAR(50),
    creative_share_final_amount VARCHAR(50),
    
    -- Part 7: หลักฐานประกอบการยื่นคำขอ
    evidence_page_charge_check BOOLEAN DEFAULT 0,
    evidence_page_charge_upload VARCHAR(300),
    evidence_full_paper_check BOOLEAN DEFAULT 0,
    evidence_full_paper_upload VARCHAR(300),
    evidence_consent_letter_check BOOLEAN DEFAULT 0,
    evidence_consent_letter_upload VARCHAR(300),
    evidence_quartile_check BOOLEAN DEFAULT 0,
    evidence_quartile_upload VARCHAR(300),
    evidence_tci_check BOOLEAN DEFAULT 0,
    evidence_tci_upload VARCHAR(300),
    evidence_editorial_board_check BOOLEAN DEFAULT 0,
    evidence_editorial_board_upload VARCHAR(300),
    evidence_exhibition_check BOOLEAN DEFAULT 0,
    evidence_exhibition_upload VARCHAR(300),
    evidence_proof_check BOOLEAN DEFAULT 0,
    evidence_proof_upload VARCHAR(300),
    evidence_nrms_check BOOLEAN DEFAULT 0,
    evidence_nrms_upload VARCHAR(300),
    evidence_other_check BOOLEAN DEFAULT 0,
    evidence_other_upload VARCHAR(300)
);

-- ตาราง settings: เก็บการตั้งค่าระบบ
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- สร้าง Index เพื่อเพิ่มประสิทธิภาพการค้นหา
CREATE INDEX IF NOT EXISTS idx_submission_created_at ON submission(created_at);
CREATE INDEX IF NOT EXISTS idx_submission_email ON submission(email);
CREATE INDEX IF NOT EXISTS idx_submission_fiscal_year ON submission(fiscal_year);
CREATE INDEX IF NOT EXISTS idx_settings_key ON settings(key);
