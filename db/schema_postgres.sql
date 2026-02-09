-- ========================================
-- R2R System Database Schema (PostgreSQL)
-- ระบบคำขอค่าตอบแทนผลงานตีพิมพ์
-- ========================================

-- ตาราง submission: เก็บข้อมูลการส่งคำขอทั้งหมด
CREATE TABLE IF NOT EXISTS submission (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    qual_1_1 BOOLEAN DEFAULT FALSE,
    qual_1_2 BOOLEAN DEFAULT FALSE,
    qual_1_3 BOOLEAN DEFAULT FALSE,
    scope_2_1 BOOLEAN DEFAULT FALSE,
    scope_2_2 BOOLEAN DEFAULT FALSE,
    scope_2_3 BOOLEAN DEFAULT FALSE,
    payment_3_1 BOOLEAN DEFAULT FALSE,
    page_charge_amount VARCHAR(50),
    payment_3_2 BOOLEAN DEFAULT FALSE,
    payment_3_3 BOOLEAN DEFAULT FALSE,
    num_institutes_3_3 VARCHAR(50),
    share_amount_3_3 VARCHAR(50),
    
    -- Part 4: ค่าตอบแทนวารสารระดับนานาชาติ
    charge_int_checkbox BOOLEAN DEFAULT FALSE,
    charge_int_amount VARCHAR(50),
    charge_int_q1q2_checkbox BOOLEAN DEFAULT FALSE,
    charge_int_q1q2_amount VARCHAR(50),
    remuneration_int_checkbox BOOLEAN DEFAULT FALSE,
    international_quartile VARCHAR(50),
    share_int_checkbox BOOLEAN DEFAULT FALSE,
    share_int_base_amount VARCHAR(50),
    share_int_num_institutes VARCHAR(50),
    share_int_final_amount VARCHAR(50),
    
    -- Part 5: วารสารพิเศษ
    special_nat_checkbox BOOLEAN DEFAULT FALSE,
    special_nat_share_checkbox BOOLEAN DEFAULT FALSE,
    special_nat_share_num_institutes VARCHAR(50),
    special_nat_share_final_amount VARCHAR(50),
    special_int_checkbox BOOLEAN DEFAULT FALSE,
    special_international_quartile VARCHAR(50),
    special_int_share_checkbox BOOLEAN DEFAULT FALSE,
    special_int_share_base_amount VARCHAR(50),
    special_int_share_num_institutes VARCHAR(50),
    special_int_share_final_amount VARCHAR(50),
    
    -- Part 6: ผลงานสร้างสรรค์
    creative_level_asean BOOLEAN DEFAULT FALSE,
    creative_level_inter_coop BOOLEAN DEFAULT FALSE,
    creative_level_national BOOLEAN DEFAULT FALSE,
    creative_level_institutional BOOLEAN DEFAULT FALSE,
    creative_level_public BOOLEAN DEFAULT FALSE,
    creative_share_checkbox BOOLEAN DEFAULT FALSE,
    creative_share_base_amount VARCHAR(50),
    creative_share_num_institutes VARCHAR(50),
    creative_share_final_amount VARCHAR(50),
    
    -- Part 7: หลักฐานประกอบการยื่นคำขอ
    evidence_page_charge_check BOOLEAN DEFAULT FALSE,
    evidence_page_charge_upload VARCHAR(300),
    evidence_full_paper_check BOOLEAN DEFAULT FALSE,
    evidence_full_paper_upload VARCHAR(300),
    evidence_consent_letter_check BOOLEAN DEFAULT FALSE,
    evidence_consent_letter_upload VARCHAR(300),
    evidence_quartile_check BOOLEAN DEFAULT FALSE,
    evidence_quartile_upload VARCHAR(300),
    evidence_tci_check BOOLEAN DEFAULT FALSE,
    evidence_tci_upload VARCHAR(300),
    evidence_editorial_board_check BOOLEAN DEFAULT FALSE,
    evidence_editorial_board_upload VARCHAR(300),
    evidence_exhibition_check BOOLEAN DEFAULT FALSE,
    evidence_exhibition_upload VARCHAR(300),
    evidence_proof_check BOOLEAN DEFAULT FALSE,
    evidence_proof_upload VARCHAR(300),
    evidence_nrms_check BOOLEAN DEFAULT FALSE,
    evidence_nrms_upload VARCHAR(300),
    evidence_other_check BOOLEAN DEFAULT FALSE,
    evidence_other_upload VARCHAR(300)
);

-- ตาราง settings: เก็บการตั้งค่าระบบ
CREATE TABLE IF NOT EXISTS settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- สร้าง Index เพื่อเพิ่มประสิทธิภาพการค้นหา
CREATE INDEX IF NOT EXISTS idx_submission_created_at ON submission(created_at);
CREATE INDEX IF NOT EXISTS idx_submission_email ON submission(email);
CREATE INDEX IF NOT EXISTS idx_submission_fiscal_year ON submission(fiscal_year);
CREATE INDEX IF NOT EXISTS idx_settings_key ON settings(key);

-- สร้าง Trigger สำหรับอัพเดทเวลาใน settings
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_settings_updated_at 
    BEFORE UPDATE ON settings 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
