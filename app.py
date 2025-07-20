import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.utils import secure_filename
from fpdf import FPDF
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash, jsonify
from fpdf.enums import Align

# --- การกำหนดค่า ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a8f5f167f44f4964e6c998dee827110c')  # Use environment variable in production
app.config['UPLOAD_FOLDER'] = 'uploads'

# สร้างโฟลเดอร์ uploads หากไม่มี
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Database configuration - ใช้ environment variable สำหรับ production
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # สำหรับ PostgreSQL บน Heroku หรือแพลตฟอร์มอื่น
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace('postgres://', 'postgresql://')
else:
    # สำหรับการทดสอบ local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

# กำหนดประเภทไฟล์ที่อนุญาต
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)
ADMIN_PASSWORD = "Publication_IRD" # รหัสผ่านสำหรับ Admin

# --- โมเดลฐานข้อมูล ---
# สร้าง Model ที่มี field ทั้งหมดจากฟอร์ม
# หมายเหตุ: ชื่อ field เป็นภาษาอังกฤษเพื่อความสะดวกในการเขียนโค้ด
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    consent_evidence_pdf = db.Column(db.String(300), nullable=True)
    
    # Part 1
    full_name = db.Column(db.String(200))
    academic_position = db.Column(db.String(200))
    affiliation = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    mobile_phone = db.Column(db.String(50))
    email = db.Column(db.String(100))

    # Part 2
    work_name_th = db.Column(db.String(300))
    work_name_en = db.Column(db.String(300))
    funding_source = db.Column(db.String(200))
    fiscal_year = db.Column(db.String(20))
    project_name = db.Column(db.String(300))
    qual_1_1 = db.Column(db.Boolean, default=False)
    qual_1_2 = db.Column(db.Boolean, default=False)
    qual_1_3 = db.Column(db.Boolean, default=False)
    scope_2_1 = db.Column(db.Boolean, default=False)
    scope_2_2 = db.Column(db.Boolean, default=False)
    payment_3_1 = db.Column(db.Boolean, default=False)
    page_charge_amount = db.Column(db.String(50))
    payment_3_2 = db.Column(db.Boolean, default=False)
    payment_3_3 = db.Column(db.Boolean, default=False)
    num_institutes_3_3 = db.Column(db.String(50))
    share_amount_3_3 = db.Column(db.String(50))
    
    # Part 4
    charge_int_checkbox = db.Column(db.Boolean, default=False)
    charge_int_amount = db.Column(db.String(50))
    remuneration_int_checkbox = db.Column(db.Boolean, default=False)
    international_quartile = db.Column(db.String(50))
    share_int_checkbox = db.Column(db.Boolean, default=False)
    share_int_base_amount = db.Column(db.String(50))
    share_int_num_institutes = db.Column(db.String(50))
    share_int_final_amount = db.Column(db.String(50))

    # Part 5
    special_nat_checkbox = db.Column(db.Boolean, default=False)
    special_nat_share_checkbox = db.Column(db.Boolean, default=False)
    special_nat_share_num_institutes = db.Column(db.String(50))
    special_nat_share_final_amount = db.Column(db.String(50))
    special_int_checkbox = db.Column(db.Boolean, default=False)
    special_international_quartile = db.Column(db.String(50))
    special_int_share_checkbox = db.Column(db.Boolean, default=False)
    special_int_share_base_amount = db.Column(db.String(50))
    special_int_share_num_institutes = db.Column(db.String(50))
    special_int_share_final_amount = db.Column(db.String(50))

    # Part 6    
    creative_level_asean = db.Column(db.Boolean, default=False)
    creative_level_inter_coop = db.Column(db.Boolean, default=False)
    creative_level_national = db.Column(db.Boolean, default=False)
    creative_level_institutional = db.Column(db.Boolean, default=False)
    creative_level_public = db.Column(db.Boolean, default=False)
    creative_share_checkbox = db.Column(db.Boolean, default=False)
    creative_share_base_amount = db.Column(db.String(50))
    creative_share_num_institutes = db.Column(db.String(50))
    creative_share_final_amount = db.Column(db.String(50))    

    # Part 7 (File Uploads)
    evidence_page_charge_check = db.Column(db.Boolean, default=False)
    evidence_page_charge_upload = db.Column(db.String(300))
    evidence_full_paper_check = db.Column(db.Boolean, default=False)
    evidence_full_paper_upload = db.Column(db.String(300))
    evidence_consent_letter_check = db.Column(db.Boolean, default=False)
    evidence_consent_letter_upload = db.Column(db.String(300))
    evidence_quartile_check = db.Column(db.Boolean, default=False)
    evidence_quartile_upload = db.Column(db.String(300))
    evidence_tci_check = db.Column(db.Boolean, default=False)
    evidence_tci_upload = db.Column(db.String(300))
    evidence_editorial_board_check = db.Column(db.Boolean, default=False)
    evidence_editorial_board_upload = db.Column(db.String(300))
    evidence_exhibition_check = db.Column(db.Boolean, default=False)
    evidence_exhibition_upload = db.Column(db.String(300))
    evidence_proof_check = db.Column(db.Boolean, default=False)
    evidence_proof_upload = db.Column(db.String(300))
    evidence_nrms_check = db.Column(db.Boolean, default=False)
    evidence_nrms_upload = db.Column(db.String(300))
    evidence_other_check = db.Column(db.Boolean, default=False)
    evidence_other_upload = db.Column(db.String(300))

# เพิ่ม Model ใหม่หลังจาก class Submission
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# --- PDF Generation  ---
class PDF(FPDF):
    def __init__(self, submission_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submission_id = submission_id  # เก็บ submission_id สำหรับใช้ในการสร้างเลขที่เอกสาร
        try:
            self.add_font('Sarabun', '', 'static/fonts/Sarabun-Regular.ttf', uni=True)
            self.add_font('Sarabun', 'B', 'static/fonts/Sarabun-Bold.ttf', uni=True)
            # vvv เพิ่มบรรทัดนี้เพื่อลงทะเบียนฟอนต์ตัวเอียง vvv
            self.add_font('Sarabun', 'I', 'static/fonts/Sarabun-Italic.ttf', uni=True)
        except RuntimeError:
            print("Font files not found. Please download...")
            pass
        self.set_font('Sarabun', '', 12)
        # เพิ่มการตั้งค่า encoding สำหรับภาษาไทย
        self.set_auto_page_break(auto=True, margin=15)

    def multi_cell(self, w, h, text, border=0, align='L', fill=False):
        # แก้ไขปัญหาสระตกโดยการปรับแต่ง multi_cell
        if isinstance(text, str):
            # ทำการ normalize text สำหรับภาษาไทย
            import unicodedata
            text = unicodedata.normalize('NFC', text)
        super().multi_cell(w, h, text, border, align, fill)

    def cell(self, w, h=0, text='', border=0, ln=0, align='', fill=False, link=''):
        # แก้ไขปัญหาสระตกโดยการปรับแต่ง cell
        if isinstance(text, str):
            # ทำการ normalize text สำหรับภาษาไทย
            import unicodedata
            text = unicodedata.normalize('NFC', text)
        super().cell(w, h, text, border, ln, align, fill, link)

    def text(self, x, y, text=''):
        # แก้ไขปัญหาสระตกโดยการปรับแต่ง text
        if isinstance(text, str):
            # ทำการ normalize text สำหรับภาษาไทย
            import unicodedata
            text = unicodedata.normalize('NFC', text)
        super().text(x, y, text)

    def header(self):
        # --- 1. เพิ่มรหัสเอกสารที่มุมบนขวา ---
        self.set_font('Sarabun', '', 9)
        self.set_text_color(128, 128, 128) # สีเทา
        # ไปที่มุมบนขวา
        self.set_y(5)
        # สร้างเลขที่เอกสารแบบอัตโนมัติ โดยใช้ submission_id จาก PDF instance
        document_number = f"ฝวน IRD_06/{self.submission_id:05d}"  # Format: IRD_06/00001, IRD_06/00002, etc.
        self.cell(0, 10, document_number, 0, 0, 'R')
        self.ln(5) # เลื่อนลงมาเล็กน้อย
        # --- 2. เพิ่มหัวข้อเอกสาร (จัดกึ่งกลาง) ---
        # กลับมาใช้ฟอนต์และสีปกติ
        self.set_font('Sarabun', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, "แบบฟอร์มขอรับการสนับสนุนการตีพิมพ์บทความวิจัย", 0, 1, 'C')        
        self.set_font('Sarabun', 'B', 12)
        self.cell(0, 8, "กองทุนส่งเสริมงานวิจัย มหาวิทยาลัยเทคโนโลยีราชมงคลธัญบุรี", 0, 1, 'C')
        self.set_font('Sarabun', 'B', 12)
        
        # ดึงการตั้งค่าหมายเหตุจากฐานข้อมูล
        setting = Settings.query.filter_by(key='header_note').first()
        header_note = setting.value if setting else "(สำหรับบทความวิจัยที่ตีพิมพ์เผยแพร่หลังวันที่ 26 กันยายน พ.ศ. 2566)"
        
        self.cell(0, 8, header_note, 0, 1, 'C')        
        # เว้นบรรทัดลงมาให้พ้นส่วน header เพื่อเริ่มเนื้อหา
        self.ln(10)

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            print("=== POST Request Received ===")
            print(f"Request files: {list(request.files.keys())}")
            print(f"Request form: {list(request.form.keys())}")
            
            # ฟังก์ชั่นผู้ช่วยในการจัดการการอัปโหลดไฟล์
            def handle_upload(field_name):
                if field_name in request.files:
                    file = request.files[field_name]
                    if file and file.filename != '':
                        print(f"Processing file: {file.filename} for field: {field_name}")
                        
                        # ตรวจสอบประเภทไฟล์
                        if not allowed_file(file.filename):
                            print(f"File type not allowed: {file.filename}")
                            return None
                        
                        filename = secure_filename(file.filename)
                        # Add timestamp to filename to avoid overwrites
                        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                        unique_filename = f"{timestamp}_{filename}"
                        
                        # Create upload directory if it doesn't exist
                        upload_dir = app.config['UPLOAD_FOLDER']
                        if not os.path.exists(upload_dir):
                            os.makedirs(upload_dir)
                            print(f"Created upload directory: {upload_dir}")
                        
                        file_path = os.path.join(upload_dir, unique_filename)
                        try:
                            file.save(file_path)
                            print(f"File saved successfully: {file_path}")
                            # ตรวจสอบว่าไฟล์ถูกสร้างจริงหรือไม่
                            if os.path.exists(file_path):
                                file_size = os.path.getsize(file_path)
                                print(f"File size: {file_size} bytes")
                                return unique_filename
                            else:
                                print(f"File was not created: {file_path}")
                                return None
                        except Exception as e:
                            print(f"Error saving file {unique_filename}: {e}")
                            return None
                else:
                    print(f"No file found for field: {field_name}")
                return None
            
            # ผู้ช่วยรับค่าช่องทำเครื่องหมาย
            def get_bool(name):
                return True if request.form.get(name) else False

            # จัดการข้อมูลตำแหน่งทางวิชาการ
            academic_position = request.form.get('academicPosition')
            if academic_position == 'อื่นๆ':
                academic_position = request.form.get('academicPositionOther', '')

            # จัดการข้อมูลสังกัด
            affiliation = request.form.get('affiliation')
            if affiliation == 'อื่นๆ':
                affiliation = request.form.get('affiliationOther', '')

            # ตรวจสอบและจำกัดค่า page_charge_amount ให้ไม่เกิน 5,000 บาท
            page_charge_amount = request.form.get('page_charge_amount')
            if page_charge_amount:
                try:
                    page_charge_value = float(page_charge_amount)
                    if page_charge_value > 5000:
                        page_charge_amount = '5000'  # จำกัดให้ไม่เกิน 5,000
                        flash('ค่าธรรมเนียมการตีพิมพ์ถูกปรับเป็น 5,000 บาท ตามเพดานที่กำหนด', 'warning')
                except ValueError:
                    pass  # ถ้าแปลงไม่ได้ ให้เก็บค่าเดิม

            new_submission = Submission(
                # Part 1
                full_name=request.form.get('fullName'),
                academic_position=academic_position,
                affiliation=affiliation,
                phone=request.form.get('phone'),
                mobile_phone=request.form.get('mobilePhone'),
                email=request.form.get('email'),

                # Part 2
                work_name_th=request.form.get('work_name_th'),
                work_name_en=request.form.get('work_name_en'),
                funding_source=request.form.get('funding_source'),
                fiscal_year=request.form.get('fiscal_year'),
                project_name=request.form.get('project_name'),
                qual_1_1=get_bool('qual_1_1'),
                qual_1_2=get_bool('qual_1_2'),
                qual_1_3=get_bool('qual_1_3'),
                scope_2_1=get_bool('scope_2_1'),
                scope_2_2=get_bool('scope_2_2'),
                payment_3_1=get_bool('payment_3_1'),
                page_charge_amount=page_charge_amount,
                payment_3_2=get_bool('payment_3_2'),
                payment_3_3=get_bool('payment_3_3'),
                num_institutes_3_3=request.form.get('num_institutes_3_3'),
                share_amount_3_3=request.form.get('share_amount_3_3'),

                # Part 4
                charge_int_checkbox=get_bool('charge_int_checkbox'),
                charge_int_amount=request.form.get('charge_int_amount'),
                remuneration_int_checkbox=get_bool('remuneration_int_checkbox'),
                international_quartile=request.form.get('international_quartile'),
                share_int_checkbox=get_bool('share_int_checkbox'),
                share_int_base_amount=request.form.get('share_int_base_amount'),
                share_int_num_institutes=request.form.get('share_int_num_institutes'),
                share_int_final_amount=request.form.get('share_int_final_amount'),
                
                # Part 5
                special_nat_checkbox=get_bool('special_nat_checkbox'),
                special_nat_share_checkbox=get_bool('special_nat_share_checkbox'),
                special_nat_share_num_institutes=request.form.get('special_nat_share_num_institutes'),
                special_nat_share_final_amount=request.form.get('special_nat_share_final_amount'),
                special_int_checkbox=get_bool('special_int_checkbox'),
                special_international_quartile=request.form.get('special_international_quartile'),
                special_int_share_checkbox=get_bool('special_int_share_checkbox'),
                special_int_share_base_amount=request.form.get('special_int_share_base_amount'),
                special_int_share_num_institutes=request.form.get('special_int_share_num_institutes'),
                special_int_share_final_amount=request.form.get('special_int_share_final_amount'),

                # Part 6
                creative_level_asean=get_bool('creative_level_asean'),
                creative_level_inter_coop=get_bool('creative_level_inter_coop'),
                creative_level_national=get_bool('creative_level_national'),
                creative_level_institutional=get_bool('creative_level_institutional'),
                creative_level_public=get_bool('creative_level_public'),

                # Part 7 (File Uploads)
                evidence_page_charge_check=get_bool('evidence_page_charge_check'),
                evidence_page_charge_upload=handle_upload('evidence_page_charge_upload'),
                evidence_full_paper_check=get_bool('evidence_full_paper_check'),
                evidence_full_paper_upload=handle_upload('evidence_full_paper_upload'),
                evidence_consent_letter_check=get_bool('evidence_consent_letter_check'),
                evidence_consent_letter_upload=handle_upload('evidence_consent_letter_upload'),
                evidence_quartile_check=get_bool('evidence_quartile_check'),
                evidence_quartile_upload=handle_upload('evidence_quartile_upload'),
                evidence_tci_check=get_bool('evidence_tci_check'),
                evidence_tci_upload=handle_upload('evidence_tci_upload'),
                evidence_editorial_board_check=get_bool('evidence_editorial_board_check'),
                evidence_editorial_board_upload=handle_upload('evidence_editorial_board_upload'),
                evidence_exhibition_check=get_bool('evidence_exhibition_check'),
                evidence_exhibition_upload=handle_upload('evidence_exhibition_upload'),
                evidence_proof_check=get_bool('evidence_proof_check'),
                evidence_proof_upload=handle_upload('evidence_proof_upload'),
                evidence_nrms_check=get_bool('evidence_nrms_check'),
                evidence_nrms_upload=handle_upload('evidence_nrms_upload'),
                evidence_other_check=get_bool('evidence_other_check'),
                evidence_other_upload=handle_upload('evidence_other_upload'),
            )
            
            print("=== File Upload Results ===")
            print(f"Page charge: {new_submission.evidence_page_charge_upload}")
            print(f"Full paper: {new_submission.evidence_full_paper_upload}")
            print(f"Consent letter: {new_submission.evidence_consent_letter_upload}")
            print(f"Quartile: {new_submission.evidence_quartile_upload}")
            print(f"TCI: {new_submission.evidence_tci_upload}")
            print(f"Editorial board: {new_submission.evidence_editorial_board_upload}")
            print(f"Exhibition: {new_submission.evidence_exhibition_upload}")
            print(f"Proof: {new_submission.evidence_proof_upload}")
            print(f"NRMS: {new_submission.evidence_nrms_upload}")
            print(f"Other: {new_submission.evidence_other_upload}")
            
            db.session.add(new_submission)
            db.session.commit()
            
            # แสดงรายชื่อไฟล์ในโฟลเดอร์ uploads
            upload_dir = app.config['UPLOAD_FOLDER']
            if os.path.exists(upload_dir):
                files_in_upload = os.listdir(upload_dir)
                print(f"Files in uploads directory: {files_in_upload}")
            else:
                print("Upload directory does not exist")
            
            return jsonify({'status': 'success', 'message': 'ส่งข้อมูลสำเร็จเรียบร้อยแล้ว!'}), 200

        except Exception as e:
            # กรณีเกิดข้อผิดพลาด ก็ตอบกลับเป็น JSON เช่นกัน
            print(f"Error on submission: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'status': 'error', 'message': 'เกิดข้อผิดพลาดในการบันทึกข้อมูล'}), 500

    # สำหรับ request แบบ GET ให้แสดงหน้าฟอร์มปกติ
    # ดึงการตั้งค่าหมายเหตุจากฐานข้อมูล
    setting = Settings.query.filter_by(key='header_note').first()
    header_note = setting.value if setting else "(สำหรับบทความวิจัยที่ตีพิมพ์เผยแพร่หลังวันที่ 26 กันยายน พ.ศ. 2566)"
    
    return render_template('index.html', header_note=header_note)

@app.route('/login', methods=['POST']) # รับเฉพาะ POST เพราะไม่มีหน้า GET แล้ว
def login():
    password = request.form.get('password')
    if password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        # ส่ง URL ของหน้า admin กลับไปให้ JavaScript
        return jsonify({'status': 'success', 'redirect_url': url_for('admin')})
    else:
        # ส่งข้อความ Error กลับไป
        return jsonify({'status': 'error', 'message': 'รหัสผ่านไม่ถูกต้อง'}), 401

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    sort_order = request.args.get('sort', 'asc', type=str)  # asc หรือ desc
    
    # สร้าง query พื้นฐาน
    query = Submission.query
    
    # เพิ่มการค้นหาตามชื่อ
    if search:
        query = query.filter(Submission.full_name.like(f'%{search}%'))
    
    # เพิ่มการเรียงลำดับ
    if sort_order == 'desc':
        query = query.order_by(Submission.id.desc())
    else:
        query = query.order_by(Submission.id.asc())
    
    pagination = query.paginate(
        page=page, per_page=20, error_out=False
    )
    
    submissions = pagination.items
    
    return render_template('admin.html', 
                         submissions=submissions, 
                         pagination=pagination,
                         search=search,
                         sort_order=sort_order)

@app.route('/download_pdf/<int:submission_id>')
def download_pdf(submission_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('index'))        
    s = Submission.query.get_or_404(submission_id)
    # ส่ง submission_id ไปยัง PDF class
    pdf = PDF(submission_id=submission_id, orientation='P', unit='mm', format='A4')
    pdf.add_page()    
    line_h = 6 # ความสูงมาตรฐานของบรรทัด
    
    # --- Helper Functions (เวอร์ชันสมบูรณ์) ---
    def draw_section_title(title):
        pdf.set_font('Sarabun', 'B', 12)
        pdf.cell(0, line_h + 2, title, 0, 1)
        pdf.ln(2)
    
    def _draw_symbol(x, y, h, symbol_type, is_checked):
        # ฟังก์ชันย่อยใหม่สำหรับวาดสัญลักษณ์โดยเฉพาะ
        box_size = 4
        box_y_pos = y + (h - box_size) / 2
        pdf.set_xy(x, y)
        if symbol_type == 'checkbox':
            pdf.rect(x, box_y_pos, box_size, box_size)
            if is_checked:
                pdf.set_font('ZapfDingbats', '', 12)
                pdf.text(x + 0.7, box_y_pos + 3, '4')
        elif symbol_type == 'radio':
            pdf.set_font('Sarabun', '', 10)
            symbol = '◉' if is_checked else '○'
            pdf.cell(box_size, h, symbol, 0, 0, 'C')

    def draw_list_item(number, text, is_checked, symbol_type='checkbox', indent=5):
        start_y = pdf.get_y()
        start_x = pdf.l_margin + indent        
        # 1. วาดลำดับข้อ
        pdf.set_font('Sarabun', '', 10)
        pdf.set_x(start_x)
        pdf.cell(10, line_h, number, 0, 0)        
        # 2. วาดสัญลักษณ์ (Checkbox หรือ Radio)
        symbol_x = pdf.get_x()
        box_size = 4
        # จัดตำแหน่งสัญลักษณ์ให้อยู่กึ่งกลางแนวตั้งของบรรทัด
        symbol_y_pos = start_y + (line_h / 2)        
        if symbol_type == 'checkbox':
            box_y_pos = symbol_y_pos - (box_size / 2)
            pdf.rect(symbol_x, box_y_pos, box_size, box_size)
            if is_checked:
                pdf.set_font('ZapfDingbats', '', 12)
                pdf.text(symbol_x + 0.7, box_y_pos + 3, '4')        
        elif symbol_type == 'radio':
            # --- ส่วนที่อัปเกรด: ใช้วาดวงกลมจริงๆ ---
            radius = 1.8 # รัศมีของวงกลม (ปรับได้)
            center_x_of_symbol = symbol_x + radius            
            # วาดวงกลมด้านนอก
            pdf.circle(center_x_of_symbol, symbol_y_pos, radius, 'D') # 'D' = Draw (วาดเส้น)            
            if is_checked:
                # ถ้าถูกเลือก ให้วาดวงกลมทึบด้านใน
                pdf.circle(center_x_of_symbol, symbol_y_pos, radius * 0.6, 'F') # 'F' = Fill ( заливка)
        # 3. วาดข้อความ
        pdf.set_font('Sarabun', '', 10)
        text_x = symbol_x + box_size + 2
        pdf.set_xy(text_x, start_y)        
        usable_width = pdf.w - pdf.r_margin - text_x
        pdf.multi_cell(usable_width, line_h, text, align='L')        
        pdf.ln(3)

    def draw_full_width_field(label, data):
        # บันทึกตำแหน่ง Y เริ่มต้นของบรรทัด
        start_y = pdf.get_y()
        # วาด Label
        pdf.set_font('Sarabun', 'B', 11)
        pdf.cell(45, line_h, label, 0, 0)
        pdf.set_font('Sarabun', '', 11)
        # --- จุดที่แก้ไข: เปลี่ยน or '' เป็น or ' ' ---
        # ใช้ multi_cell เพื่อรองรับข้อความยาวๆ และใช้ ' ' เป็นค่าสำรอง
        pdf.multi_cell(0, line_h, f": {data or ' '}", border='B', align='L')
        y_after = pdf.get_y()
        pdf.set_y(max(start_y + line_h, y_after))
        pdf.ln(3)

    def draw_checkbox(text, checked, indent=0):
        usable_width = pdf.w - pdf.l_margin - pdf.r_margin
        # ตำแหน่งเริ่มต้นในการวาด จะบวกค่าย่อหน้าที่รับเข้ามา
        start_x = pdf.l_margin + indent        
        # บันทึกตำแหน่ง Y ปัจจุบัน
        start_y = pdf.get_y()        
        # วาดกล่องสี่เหลี่ยมที่ตำแหน่งซึ่งย่อหน้าเข้ามาแล้ว
        pdf.set_x(start_x)
        box_size = 4 # ขนาดของกล่อง
        pdf.rect(start_x, start_y + 0.5, box_size, box_size)        
        if checked:
            pdf.set_font('ZapfDingbats', '', 12)
            pdf.text(start_x + 0.7, start_y + 3.5, '4') # '4' คือเครื่องหมายถูก        
        # กลับมาใช้ฟอนต์ปกติเพื่อวาดข้อความ
        pdf.set_font('Sarabun', '', 10)        
        # วาดข้อความต่อจากกล่อง
        pdf.set_xy(start_x + box_size + 2, start_y)
        # คำนวณความกว้างที่เหลือสำหรับข้อความ
        text_width = usable_width - indent - box_size - 2
        pdf.multi_cell(text_width, 5, text, align='L')
        
    # ==================================
    # === START RENDERING PDF DOCUMENT ===
    # ==================================
   
    # --- 1. ประวัติผู้ขอรับการสนับสนุน ---
    draw_section_title("ประวัติผู้ขอรับการสนับสนุน")    
    # คำนวณความกว้างที่ใช้งานได้ของหน้ากระดาษ
    usable_width = pdf.w - pdf.l_margin - pdf.r_margin    
    # --- บรรทัดที่ 1: ชื่อ-สกุล และ ตำแหน่งทางวิชาการ (2 คอลัมน์) ---
    col_width_2 = usable_width / 2
    label_width_2 = 40 # ความกว้างของป้ายกำกับ
    # คอลัมน์ที่ 1: ชื่อ-สกุล
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(label_width_2, line_h, "ชื่อ-สกุล:", 0, 0)
    pdf.set_font('Sarabun', '', 11)
    pdf.cell(col_width_2 - label_width_2, line_h, f"{s.full_name or ''}", border='', ln=0, align='C')    
    # คอลัมน์ที่ 2: ตำแหน่งทางวิชาการ
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(label_width_2, line_h, "ตำแหน่งทางวิชาการ:", 0, 0, '') # จัดป้ายชิดขวา
    pdf.set_font('Sarabun', '', 11)
    pdf.cell(col_width_2 - label_width_2, line_h, f"{s.academic_position or ''}", border='', ln=1, align='C')
    # --- บรรทัดที่ 2: สังกัด (1 คอลัมน์เต็ม) ---
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(label_width_2, line_h, "สังกัด:", 0, 0)
    pdf.set_font('Sarabun', '', 11)
    pdf.cell(0, line_h, f"{s.affiliation or ''}", border='B', ln=1, align='L')
    # --- บรรทัดที่ 3: ข้อมูลติดต่อ (3 คอลัมน์) ---
    col_width_3 = usable_width / 3
    label_width_3 = 25
    # คอลัมน์ที่ 1: โทรศัพท์
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(label_width_3, line_h, "โทรศัพท์:", 0, 0)
    pdf.set_font('Sarabun', '', 11)
    pdf.cell(col_width_3 - label_width_3, line_h, f"{s.phone or ''}", border='B', ln=0, align='C')    
    # คอลัมน์ที่ 2: โทรศัพท์มือถือ
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(label_width_3, line_h, "โทรศัพท์มือถือ:", 0, 0, 'R')
    pdf.set_font('Sarabun', '', 11)
    pdf.cell(col_width_3 - label_width_3, line_h, f"{s.mobile_phone or ''}", border='B', ln=0, align='C')    
    # คอลัมน์ที่ 3: อีเมล์
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(label_width_3 - 10, line_h, "อีเมล์:", 0, 0, 'R')
    pdf.set_font('Sarabun', '', 11)
    pdf.cell(col_width_3 - (label_width_3 - 10), line_h, f"{s.email or ''}", border='B', ln=1, align='C')
    pdf.ln(5) # เว้นบรรทัดก่อนเริ่มส่วนถัดไป

    # --- 2. รายละเอียดผลงาน (กรุณาขีดเครื่องหมาย ✓ หน้าข้อความที่ตรงกับคุณสมบัติ) ---
    draw_section_title("รายละเอียดผลงาน")
    draw_full_width_field("ชื่อผลงาน/บทความ (ไทย):",  s.work_name_th) 
    draw_full_width_field("ชื่อผลงาน/บทความ (อังกฤษ):",  s.work_name_en) 
    # --- บรรทัด แหล่งงบประมาณ และ ปีงบประมาณ (จัดแบบ 2 คอลัมน์) ---
    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_width_2 = usable_width / 2
    label_width = 50

    start_y = pdf.get_y()

    # คอลัมน์ที่ 1: แหล่งงบประมาณ
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(label_width, line_h, "แหล่งงบประมาณที่ใช้ในการวิจัย:", 0, 0)
    pdf.set_font('Sarabun', '', 11)
    # --- จุดที่แก้ไข: เปลี่ยน or '' เป็น or ' ' ---
    pdf.cell(col_width_2 - label_width, line_h, f"{s.funding_source or ' '}", border='B', ln=0, align='C')

    # คอลัมน์ที่ 2: ปีงบประมาณ
    pdf.set_xy(pdf.l_margin + col_width_2, start_y)
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(label_width - 20, line_h, "ประจำปีงบประมาณ:", 0, 0, 'R')
    pdf.set_font('Sarabun', '', 11)
    # --- จุดที่แก้ไข: เปลี่ยน or '' เป็น or ' ' ---
    pdf.cell(col_width_2 - (label_width - 20), line_h, f"{s.fiscal_year or ' '}", border='B', ln=1, align='C')
    # --- ส่วนที่ 3  ---    
    # 1. คุณสมบัติของผู้ขอรับการสนับสนุนฯ (เรียกใช้ draw_checkbox พร้อมค่าย่อหน้า)
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(0, 6, "1. คุณสมบัติของผู้ขอรับการสนับสนุนการตีพิมพ์บทความวิจัยฯ", 0, 1)
    pdf.ln(2)
    # --- ข้อมูลคุณสมบัติทั้งหมด ---
    qualifications = [
        ("1.1", "เป็นนักวิจัยของมหาวิทยาลัย และปฏิบัติราชการเต็มเวลามาแล้วไม่น้อยกว่า 9 เดือน โดยนับตั้งแต่วันที่ได้รับการบรรจุและแต่งตั้ง จนถึงวันที่เสนอขอรับการสนับสนุน และไม่อยู่ระหว่างลาศึกษาต่อ", s.qual_1_1),
        ("1.2", "เป็นผู้เขียนชื่อแรก (First author) หรือเป็นผู้รับผิดชอบหลัก (Corresponding author) ที่ระบุชื่อหน่วยงานของมหาวิทยาลัยเทคโนโลยีราชมงคลธัญบุรี ที่ตำแหน่งที่อยู่ของผู้เขียนปรากฏในบทความอย่างชัดเจน และปรากฏ E-mail ติดต่อผู้เขียนด้วย E-mail มหาวิทยาลัย (กรณีที่ทั้งผู้เขียนชื่อแรกและผู้เขียนชื่อหลักมีคุณสมบัติตามข้อ 1.1 จะให้การสนับสนุนเฉพาะ ผู้เขียนชื่อแรก แต่ถ้าผู้เขียนที่เป็นชื่อหลักมีความประสงค์จะขอรับการสนับสนุนแทนจะต้องมีหนังสือยินยอมจากผู้เขียนชื่อแรกแนบพร้อมแบบฟอร์ม IRD_06)", s.qual_1_2),
        ("1.3", "กรณีเผยแพร่งานสร้างสรรค์ ต้องมีชื่อผู้สร้างสรรค์เป็นผู้จัดทำ พร้อมทั้งระบุชื่อมหาวิทยาลัย เทคโนโลยีราชมงคลธัญบุรีไว้ที่ตำแหน่งที่อยู่ของผลงานสร้างสรรค์ด้วย", s.qual_1_3)
    ]    
    for number, text, is_checked in qualifications:
        start_y = pdf.get_y()        
        # 1. วาดลำดับข้อ
        pdf.set_font('Sarabun', '', 10)
        pdf.set_x(pdf.l_margin + 5) # ย่อหน้าเข้ามา 5mm
        pdf.cell(10, line_h, number, 0, 0)        
        # 2. วาด Checkbox
        box_x = pdf.get_x()
        box_size = 4
        # จัดตำแหน่งกล่องให้อยู่กึ่งกลางความสูงของบรรทัด
        pdf.rect(box_x, start_y + (line_h - box_size) / 2, box_size, box_size)
        if is_checked:
            pdf.set_font('ZapfDingbats', '', 12)
            pdf.text(box_x + 0.7, start_y + (line_h / 2) + (box_size / 4), '4')
            pdf.set_font('Sarabun', '', 10)
        # 3. วาดข้อความ
        text_x = box_x + box_size + 2
        pdf.set_xy(text_x, start_y)        
        # คำนวณความกว้างที่เหลือสำหรับข้อความ
        usable_width = pdf.w - pdf.r_margin - text_x
        pdf.multi_cell(usable_width, line_h, text, align='L')        
        # เว้นบรรทัดให้พอดีกับความสูงของข้อความที่วาดไป
        pdf.ln(3)
    pdf.ln(10)

    # 2. ขอบเขตของบทความวิจัยหรืองานสร้างสรรค์ที่ขอรับการสนับสนุน
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(0, 6, "2. ขอบเขตของบทความวิจัยหรืองานสร้างสรรค์ที่ขอรับการสนับสนุน", 0, 1)
    pdf.ln(2)
    # --- ข้อมูลขอบเขต ---
    scopes = [
        ("2.1", "เป็นบทความวิจัยหรืองานสร้างสรรค์ที่ไม่เคยเผยแพร่ที่ใดมาก่อนหรือเผยแพร่ไม่เกิน 1 ปี หมายเหตุ บทความใดที่ได้ลงตีพิมพ์ในการประชุมวิชาการ และถูกคัดเลือกมาลงในวารสาร (Journal) สามารถขอรับการสนับสนุนได้เพียงอย่างเดียว", s.scope_2_1),
        ("2.2", "บทความวิจัยที่ขอรับการสนับสนุนต้องไม่เป็นส่วนหนึ่งของผลงานวิจัยที่สำเร็จการศึกษาของผู้รับการสนับสนุนผลงานวิจัย และไม่รวมถึงจดหมายถึงบรรณาธิการ (Letter to editor,Short communication note) หรืองานเขียนขึ้นที่ลักษณะคล้ายกับที่กล่าวข้างต้น", s.scope_2_2)
    ]    
    for number, text, is_checked in scopes:
        # บันทึกตำแหน่ง Y เริ่มต้นของแถว
        start_y = pdf.get_y()        
        # 1. วาดลำดับข้อ
        pdf.set_font('Sarabun', '', 10)
        pdf.set_x(pdf.l_margin + 5) # ย่อหน้าเข้ามา 5mm
        pdf.cell(10, line_h, number, 0, 0)        
        # 2. วาด Checkbox
        box_x = pdf.get_x()
        box_size = 4
        # จัดตำแหน่งกล่องให้อยู่กึ่งกลางความสูงของบรรทัด
        pdf.rect(box_x, start_y + (line_h - box_size) / 2, box_size, box_size)
        if is_checked:
            pdf.set_font('ZapfDingbats', '', 12)
            pdf.text(box_x + 0.7, start_y + (line_h / 2) + (box_size / 4), '4')
            pdf.set_font('Sarabun', '', 10)
        # 3. วาดข้อความ
        text_x = box_x + box_size + 2
        pdf.set_xy(text_x, start_y)        
        # คำนวณความกว้างที่เหลือสำหรับข้อความ
        usable_width = pdf.w - pdf.r_margin - text_x
        pdf.multi_cell(usable_width, line_h, text, align='L')        
        # เว้นบรรทัดให้พอดี
        pdf.ln(3)
    pdf.ln(10)

    # 3. หลักเกณฑ์การจ่ายเงิน (ระดับชาติ)
    pdf.add_page() 
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(0, 6, "3. หลักเกณฑ์การจ่ายเงินฯ กรณีตีพิมพ์ในวารสารระดับชาติ", 0, 1)
    pdf.ln(2)
    # --- สร้างลิสต์ข้อมูลสำหรับส่วนที่ 3 ---
    placeholder = ".........." # ตัวแปรสำหรับเก็บเส้นประ    
    # แก้ไข f-string ให้ใช้ placeholder แทน 'N/A'
    text_3_1 = f"ค่าธรรมเนียมการตีพิมพ์บทความวิจัย (Page charge) ของวารสารที่อยู่ในฐานข้อมูล TCI ตามที่จ่ายจริงแต่ไม่เกิน 5,000 บาท ต่อเรื่อง (ระบุ: {s.page_charge_amount or placeholder} บาท)"
    text_3_2 = "ค่าสมนาคุณการตีพิมพ์บทความวิจัยในวารสารระดับชาติที่อยู่ในฐานข้อมูล TCI กลุ่ม 1 หรือ กลุ่ม 2 จ่ายเงินค่าสมนาคุณการตีพิมพ์บทความวิจัย 4,000 บาท"
    text_3_3 = f"กรณีผู้ขอรับการสนับสนุนเขียนบทความวิจัยโดยทำงานร่วมกับสถาบันอื่น จะจ่ายค่าสมนาคุณฯตามสัดส่วน ในการรับเงินสนับสนุน 4,000 บาท (คำนวณ: {s.num_institutes_3_3 or placeholder} สถาบัน = {s.share_amount_3_3 or placeholder} บาท)"    
    payments_nat = [
        ("3.1", text_3_1, s.payment_3_1),
        ("3.2", text_3_2, s.payment_3_2),
        ("3.3", text_3_3, s.payment_3_3)
    ]    
    # --- วาดทุกรายการเหมือนส่วนที่ 2 ---
    for number, text, is_checked in payments_nat:
        # บันทึกตำแหน่ง Y เริ่มต้นของแถว
        start_y = pdf.get_y()        
        # 1. วาดลำดับข้อ
        pdf.set_font('Sarabun', '', 10)
        pdf.set_x(pdf.l_margin + 5)
        pdf.cell(10, line_h, number, 0, 0)        
        # 2. วาด Checkbox
        box_x = pdf.get_x()
        box_size = 4
        pdf.rect(box_x, start_y + (line_h - box_size) / 2, box_size, box_size)
        if is_checked:
            pdf.set_font('ZapfDingbats', '', 12)
            pdf.text(box_x + 0.7, start_y + (line_h / 2) + (box_size / 4), '4')
            pdf.set_font('Sarabun', '', 10)
        # 3. วาดข้อความ
        text_x = box_x + box_size + 2
        pdf.set_xy(text_x, start_y)        
        usable_width_for_text = pdf.w - pdf.r_margin - text_x
        pdf.multi_cell(usable_width_for_text, line_h, text, align='L')        
        pdf.ln(3)
   
     # 4. หลักเกณฑ์การจ่ายเงินฯ กรณีตีพิมพ์ในวารสารระดับนานาชาติ
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(0, 6, "4. หลักเกณฑ์การจ่ายเงินฯ กรณีตีพิมพ์ในวารสารระดับนานาชาติ", 0, 1)
    pdf.ln(2)
    # กำหนดค่าย่อหน้าและเส้นประ
    item_indent = 5
    sub_item_indent = 15
    placeholder = ".........."
    # --- 4.1 ---
    text_4_1 = f"ค่าธรรมเนียมที่ทางวารสารเรียกเก็บเพื่อการตีพิมพ์ (Page charge)... สนับสนุนตามที่จ่ายจริง แต่ไม่เกิน 10,000 บาท ต่อเรื่อง (ระบุ: {s.charge_int_amount or placeholder} บาท)"
    draw_list_item("4.1", text_4_1, s.charge_int_checkbox, indent=item_indent)
    pdf.ln(2)
    # --- 4.2 ---
    text_4_2_main = "ค่าสมนาคุณการตีพิมพ์บทความวิจัยในวารสารระดับนานาชาติให้ใช้ค่าควอไทล์ที่ปรากฎใน ฐานข้อมูลการ จัดอันดับวารสาร Scopus โดยพิจารณาจากปีล่าสุดที่ปรากฎอยู่ในฐานข้อมูล ณ วันที่บทความได้รับการ ตีพิมพ์ ดังนี้"
    draw_list_item("4.2", text_4_2_main, s.remuneration_int_checkbox, indent=item_indent)
    # --- รายการย่อยของ 4.2 (Radio Buttons) ---
    quartile_map = {
        'top10': 'Top 10% หรือ Tier 1 (สนับสนุน 60,000 บาท)',
        'q1': 'ควอไทล์ที่ 1 (Q1) (สนับสนุน 30,000 บาท)',
        'q2': 'ควอไทล์ที่ 2 (Q2) (สนับสนุน 20,000 บาท)',
        'q3': 'ควอไทล์ที่ 3 (Q3) (สนับสนุน 10,000 บาท)',
        'q4': 'ควอไทล์ที่ 4 (Q4) (สนับสนุน 8,000 บาท)',
        'none': 'ไม่มีควอไทล์ (สนับสนุน 4,000 บาท)'
    }
    for value, text in quartile_map.items():
        is_selected = (s.international_quartile == value)
        draw_list_item("", text, is_selected, symbol_type='radio', indent=sub_item_indent)    
    # --- รายการย่อยของ 4.2 (การหาร) ---
    # แก้ไข f-string ให้ใช้ placeholder
    text_4_2_share = f"กรณีทำงานร่วมกับสถาบันอื่น (นานาชาติ) จะจ่ายค่าสมนาคุณตามสัดส่วน (คำนวณ: ฐาน {s.share_int_base_amount or placeholder} / {s.share_int_num_institutes or placeholder} สถาบัน = {s.share_int_final_amount or placeholder} บาท)"
    # แสดงตัวเลือกการแบ่งสัดส่วนเสมอ
    draw_list_item("", text_4_2_share, s.share_int_checkbox, indent=sub_item_indent)
    pdf.ln(5)
    
      # 5. กรณีตีพิมพ์ในวารสารประเภทบทความวิจัยที่ถูกคัดเลือกฯ (Special Issue)
    pdf.add_page()
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(0, 6, "5. กรณีตีพิมพ์ในวารสารประเภทบทความวิจัยที่ถูกคัดเลือกฯ (Special Issue)", 0, 1)
    pdf.ln(2)
    # กำหนดค่าย่อหน้าและเส้นประ
    item_indent = 5
    sub_item_indent = 15
    placeholder = ".........."
    # --- 5.1 ---
    text_5_1_main = "กรณีวารสารระดับชาติและปรากฏในฐานข้อมูลTCI สนับสนุน 1,000 บาท"
    draw_list_item("5.1", text_5_1_main, s.special_nat_checkbox, indent=item_indent)
    # --- รายการย่อยของ 5.1 ---
    text_5_1_share = f"กรณีผู้ขอรับการสนับสนุนเขียนบทความวิจัยโดยทำงานร่วมกับสถาบันอื่น...ตามสัดส่วน (คำนวณ: 1000 / {s.special_nat_share_num_institutes or placeholder} สถาบัน = {s.special_nat_share_final_amount or placeholder} บาท)"
    # จะแสดงผลก็ต่อเมื่อข้อ 5.1 ถูกเลือก
    if s.special_nat_checkbox:
        draw_list_item("", text_5_1_share, s.special_nat_share_checkbox, indent=sub_item_indent)
    pdf.ln(2)
    # --- 5.2 ---
    text_5_2_main = "กรณีวารสารระดับนานาชาติและปรากฏในฐานข้อมูลสากล สนับสนุน 1 ใน 4 ของข้อ 4.2"
    draw_list_item("5.2", text_5_2_main, s.special_int_checkbox, indent=item_indent)    
    # --- รายการย่อยของ 5.2 ---
    # จะแสดงผลก็ต่อเมื่อข้อ 5.2 ถูกเลือก
    if s.special_int_checkbox:
        special_quartile_map = {
            'top10': 'Top 10% หรือ Tier 1 (15,000 บาท)',
            'q1': 'ควอไทล์ที่ 1 (Q1) (7,500 บาท)',
            'q2': 'ควอไทล์ที่ 2 (Q2) (5,000 บาท)',
            'q3': 'ควอไทล์ที่ 3 (Q3) (2,500 บาท)',
            'q4': 'ควอไทล์ที่ 4 (Q4) (2,000 บาท)',
            'none': 'ไม่มีควอไทล์ (1,000 บาท)'
        }
        for value, text in special_quartile_map.items():
            is_selected = (s.special_international_quartile == value)
            draw_list_item("", text, is_selected, symbol_type='radio', indent=sub_item_indent)
        # การหารสัดส่วน
        text_5_2_share = f"กรณีทำงานร่วมกับสถาบันอื่น (นานาชาติ): ฐาน {s.special_int_share_base_amount or placeholder} / {s.special_int_share_num_institutes or placeholder} สถาบัน = {s.special_int_share_final_amount or placeholder} บาท"
        draw_list_item("", text_5_2_share, s.special_int_share_checkbox, indent=sub_item_indent)
    pdf.ln(5)

     # 6. ค่าสมนาคุณงานสร้างสรรค์ที่เผยแพร่
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(0, 6, "6. ค่าสมนาคุณงานสร้างสรรค์ที่เผยแพร่", 0, 1)
    pdf.ln(2)
    # กำหนดค่าย่อหน้าและเส้นประ
    item_indent = 5
    sub_item_indent = 15
    placeholder = ".........."
    # --- สร้างลิสต์ข้อมูลสำหรับส่วนที่ 6 ---
    creative_options = [
        ("6.1", "งานสร้างสรรค์ที่เผยแพร่ในระดับภูมิภาคอาเซียน/นานาชาติ (8,000 บาท)", s.creative_level_asean),
        ("6.2", "งานสร้างสรรค์ที่เผยแพร่ในระดับความร่วมมือระหว่างประเทศ (4,000 บาท)", s.creative_level_inter_coop),
        ("6.3", "งานสร้างสรรค์ที่เผยแพร่ในระดับชาติ (3,000 บาท)", s.creative_level_national),
        ("6.4", "งานสร้างสรรค์ที่เผยแพร่ในระดับสถาบัน (1,500 บาท)", s.creative_level_institutional),
        ("6.5", "งานสร้างสรรค์ที่เผยแพร่สู่สาธารณะในลักษณะใดลักษณะหนึ่งหรือผ่านสื่ออิเล็กทรอนิกส์ (1,000 บาท)", s.creative_level_public)
    ]
    # --- วาดทุกรายการ ---
    for number, text, is_checked in creative_options:
        draw_list_item(number, text, is_checked, indent=item_indent)    
    pdf.ln(2)
    # --- รายการย่อย (การหาร) ---
    # แก้ไข f-string ให้ใช้ placeholder แทน 'N/A'
    text_share = f"กรณีทำงานร่วมกับสถาบันอื่น จะจ่ายค่าสมนาคุณตามสัดส่วน (คำนวณ: ฐาน {s.creative_share_base_amount or placeholder} / {s.creative_share_num_institutes or placeholder} สถาบัน = {s.creative_share_final_amount or placeholder} บาท)"
    draw_list_item("", text_share, s.creative_share_checkbox, indent=sub_item_indent)    
    pdf.ln(5)

    # 7. หลักฐานประกอบการเสนอขอรับการสนับสนุน
    pdf.add_page()
    pdf.set_font('Sarabun', 'B', 11)
    pdf.cell(0, 6, "7. หลักฐานประกอบการเสนอขอรับการสนับสนุน", 0, 1)
    pdf.ln(2)
    item_indent = 5 # กำหนดค่าย่อหน้า
    # --- สร้างลิสต์ข้อมูลสำหรับส่วนที่ 7 ---
    file_fields = [
        ("7.1", "ค่าธรรมเนียมที่ทางวารสารเรียกเก็บเพื่อการตีพิมพ์ (Page charge) ที่ระบุชื่อผู้จ่ายเงินเป็นนักวิจัยที่ขอรับการ สนับสนุน พร้อมแนบหลักฐานแสดงการชำระเงิน (ตัวจริง)", s.evidence_page_charge_check),
        ("7.2", "สำเนาหลักฐานการตีพิมพ์ (Full Paper) ที่มี Volume และเลขหน้า หรือเลข DOI พร้อมหน้าปกวารสาร", s.evidence_full_paper_check),
        ("7.3", "หนังสือยินยอมและสำเนาบัตรประชาชนของผู้เขียนชื่อแรก (กรณีที่ไม่ใช่ผู้เขียนชื่อแรก)", s.evidence_consent_letter_check),
        ("7.4", "หลักฐานการอ้างอิงค่าควอไทล์ (Journal Quartile Score) และหลักฐานที่แสดงวารสารนั้นปรากฏใน ฐานข้อมูลสากล Scopus กรณีวารสารระดับนานาชาติ ", s.evidence_quartile_check),
        ("7.5", "หลักฐานจากฐานข้อมูล TCI กลุ่ม 1 หรือ 2 กรณีวารสารระดับชาติ", s.evidence_tci_check),
        ("7.6", "รายชื่อกองบรรณาธิการ (Editorial board) ของบทความวิจัยและบทความวิชาการทั้งระดับชาติ และนานาชาต", s.evidence_editorial_board_check),
        ("7.7", "สูจิบัตรหรือสำเนาการจัดนิทรรศการ หรือการแสดงผลงาน กรณีงานสร้างสรรค์ทีเผยแพร่", s.evidence_exhibition_check),
        ("7.8", "หลักฐานของผลงานที่นำไปเผยแพร่ เช่น รูปเล่มรายงาน, รูปถ่าย เป็นต้น", s.evidence_proof_check),
        ("7.9", "เอกสารแสดงการส่งเล่มรายงานฉบับสมบูรณ์และปิดโครงการในระบบ NRMS หรือ DRMS", s.evidence_nrms_check),
        ("7.10", "เอกสารอื่นๆตามที่สถาบันวิจัยและพัฒนากำหนด", s.evidence_other_check),
    ]
    # --- วาดทุกรายการ ---
    for number, text, is_checked in file_fields:
        draw_list_item(number, text, is_checked, indent=item_indent)    
    # วาดไฟล์แนบท้ายสุด (ถ้ามี)
    if s.consent_evidence_pdf:
        draw_list_item("7.11", "หลักฐานเพิ่มเติม (หนังสือยินยอม)", True, indent=item_indent)
    pdf.ln(5)

    # --- ข้อความรับรอง (ใหม่) ---
    pdf.ln(10) # เพิ่มระยะห่างจากส่วนบน
    pdf.set_font('Sarabun', 'B', 11)
    certification_text = "ขอรับรองว่าข้อความข้างต้นเป็นความจริงและได้แนบหลักฐานประกอบครบถ้วนเพื่อรับการสนับสนุน"
    pdf.multi_cell(0, line_h, certification_text, align='C')
    pdf.ln(10) # เพิ่มระยะห่างก่อนส่วนลงนาม

    # --- สร้างและส่งไฟล์ PDF ---
    # แก้ไขการตั้งชื่อไฟล์ให้ใช้ชื่อผลงาน และชื่อผู้ขอรับการสนับสนุน
    work_name = s.work_name_th or s.work_name_en or "ผลงาน"
    applicant_name = s.full_name or "ผู้ขอรับการสนับสนุน"
    
    # ทำความสะอาดชื่อไฟล์ (ลบอักขระที่ไม่เหมาะสม)
    work_name_clean = "".join(c for c in work_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    applicant_name_clean = "".join(c for c in applicant_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    
    pdf_filename = f"{work_name_clean}_{applicant_name_clean}.pdf"
    
    # กำหนดโฟลเดอร์ปลายทาง - ลองหาโฟลเดอร์ Downloads ของ Admin
    try:
        # สำหรับ Windows
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(downloads_dir):
            # ถ้าหา Downloads ไม่เจอ ให้ใช้ Desktop แทน
            downloads_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(downloads_dir):
            # ถ้าหา Desktop ก็ไม่เจอ ให้ใช้ current directory
            downloads_dir = os.getcwd()
    except:
        # ถ้าเกิดข้อผิดพลาดใดๆ ให้ใช้ current directory
        downloads_dir = os.getcwd()
    
    # บันทึกไฟล์ PDF ลงในโฟลเดอร์ปลายทาง
    pdf_path = os.path.join(downloads_dir, pdf_filename)
    pdf.output(pdf_path)
    
    # ส่งไฟล์ให้ดาวน์โหลด
    return send_from_directory(downloads_dir, pdf_filename, as_attachment=True)

# --- สำหรับเปิดดูไฟล์ที่อัปโหลด ---
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    if not session.get('admin_logged_in'):
        return redirect(url_for('index'))
    # ส่งไฟล์จากโฟลเดอร์ uploads กลับไป
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- สำหรับดึงข้อมูลไปแสดงใน Popup ---
@app.route('/submission/<int:submission_id>')
def get_submission(submission_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401    
    
    submission = Submission.query.get_or_404(submission_id)
    
    # แปลงข้อมูล object เป็น dictionary เพื่อส่งกลับเป็น JSON
    # โค้ดนี้จะดึงข้อมูลทุกคอลัมน์มาโดยอัตโนมัติ
    submission_data = {c.name: getattr(submission, c.name) for c in submission.__table__.columns}
    
    # แปลง object datetime เป็น string ก่อนส่ง
    if submission_data.get('created_at'):
        submission_data['created_at'] = submission_data['created_at'].isoformat()
    if submission_data.get('consent_date'):
        # ตรวจสอบเพิ่มเติมเผื่อเป็น string อยู่แล้ว
        if hasattr(submission_data['consent_date'], 'isoformat'):
            submission_data['consent_date'] = submission_data['consent_date'].isoformat()

    return jsonify(submission_data)

# --- ฟังก์ชันใหม่สำหรับลบข้อมูล ---
@app.route('/delete/<int:submission_id>', methods=['POST'])
def delete_submission(submission_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('index'))

    submission = Submission.query.get_or_404(submission_id)
    deleted_id = submission.id

    # ลิสต์ของ field ทั้งหมดที่เก็บชื่อไฟล์อัปโหลด
    file_fields_to_delete = [
        'evidence_page_charge_upload', 'evidence_full_paper_upload',
        'evidence_consent_letter_upload', 'evidence_quartile_upload',
        'evidence_tci_upload', 'evidence_editorial_board_upload',
        'evidence_exhibition_upload', 'evidence_proof_upload',
        'evidence_nrms_upload', 'evidence_other_upload',
        'consent_evidence_pdf'
    ]

    # ทำการลบไฟล์จริงๆ ออกจากโฟลเดอร์ uploads
    for field in file_fields_to_delete:
        if hasattr(submission, field):
            filename = getattr(submission, field)
            if filename:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                except OSError as e:
                    print(f"Error deleting file {filename}: {e}")
        else:
            print(f"Warning: Field '{field}' does not exist in Submission model")

    # ลบข้อมูลออกจากฐานข้อมูล
    db.session.delete(submission)
    db.session.commit()

    # หาข้อมูลทั้งหมดที่มี ID มากกว่า ID ที่ถูกลบ และจัดเรียงตาม ID
    submissions_to_update = Submission.query.filter(Submission.id > deleted_id).order_by(Submission.id).all()
    
    # อัปเดต ID ของข้อมูลที่เหลือให้เรียงต่อกัน โดยใช้ raw SQL
    for submission in submissions_to_update:
        old_id = submission.id
        new_id = old_id - 1
        
        try:
            # ใช้ text() สำหรับ raw SQL ใน SQLAlchemy 2.x
            db.session.execute(
                text("UPDATE submission SET id = :new_id WHERE id = :old_id"),
                {"new_id": new_id, "old_id": old_id}
            )
        except Exception as e:
            print(f"Error updating ID from {old_id} to {new_id}: {e}")
            db.session.rollback()
            flash('เกิดข้อผิดพลาดในการจัดเรียง ID ใหม่', 'error')
            return redirect(url_for('admin'))
    
    # Commit การเปลี่ยนแปลง
    try:
        db.session.commit()
        
        # รีเซ็ต AUTO_INCREMENT สำหรับ SQLite
        max_id_result = db.session.execute(text("SELECT MAX(id) FROM submission")).fetchone()
        max_id = max_id_result[0] if max_id_result[0] else 0
        
        # รีเซ็ต sequence สำหรับ SQLite
        db.session.execute(text(f"UPDATE sqlite_sequence SET seq = {max_id} WHERE name = 'submission'"))
        db.session.commit()
        
        flash('ลบข้อมูลเรียบร้อยแล้ว', 'success')
    except Exception as e:
        print(f"Error during final commit or auto increment reset: {e}")
        db.session.rollback()
        flash('เกิดข้อผิดพลาดในการลบข้อมูล', 'error')

    return redirect(url_for('admin'))

# เพิ่ม Routes ใหม่หลังจาก @app.route('/admin')
@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    if not session.get('admin_logged_in'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        header_note = request.form.get('header_note')
        
        # อัปเดตหรือสร้างการตั้งค่าใหม่
        setting = Settings.query.filter_by(key='header_note').first()
        if setting:
            setting.value = header_note
            setting.updated_at = datetime.utcnow()
        else:
            setting = Settings(key='header_note', value=header_note)
            db.session.add(setting)
        
        db.session.commit()
        flash('อัปเดตการตั้งค่าเรียบร้อยแล้ว', 'success')
        return redirect(url_for('admin_settings'))
    
    # ดึงการตั้งค่าปัจจุบัน
    setting = Settings.query.filter_by(key='header_note').first()
    current_note = setting.value if setting else "(สำหรับบทความวิจัยที่ตีพิมพ์เผยแพร่หลังวันที่ 26 กันยายน พ.ศ. 2566)"
    
    return render_template('admin_settings.html', current_note=current_note)

@app.errorhandler(413)
def too_large(e):
    return jsonify({'status': 'error', 'message': 'ไฟล์ใหญ่เกินไป (ขนาดสูงสุด 16 MB)'}), 413

@app.route('/test_upload')
def test_upload():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Test Upload</title></head>
    <body>
        <h1>Test File Upload</h1>
        <form method="post" enctype="multipart/form-data" action="/">
            <label>Name:</label><br>
            <input type="text" name="fullName" value="Test User" required><br><br>
            
            <label>Affiliation:</label><br>
            <input type="text" name="affiliation" value="Test University" required><br><br>
            
            <label>Page Charge Evidence:</label><br>
            <input type="checkbox" name="evidence_page_charge_check" checked>
            <input type="file" name="evidence_page_charge_upload" accept=".pdf"><br><br>
            
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """

if __name__ == '__main__':
    with app.app_context():
        # สร้างตารางหากไม่มีอยู่จริง
        db.create_all()
        
        # ตรวจสอบและสร้างการตั้งค่าเริ่มต้นหากจำเป็น
        try:
            existing_setting = Settings.query.filter_by(key='header_note').first()
            if not existing_setting:
                default_setting = Settings(
                    key='header_note', 
                    value='(สำหรับบทความวิจัยที่ตีพิมพ์เผยแพร่หลังวันที่ 26 กันยายน พ.ศ. 2566)'
                )
                db.session.add(default_setting)
                db.session.commit()
                print("Default settings created.")
            else:
                print("Settings already exist.")
        except Exception as e:
            db.session.rollback()
            print(f"Settings initialization error: {e}")
    
    # สร้างโฟลเดอร์อัปโหลดหากไม่มีอยู่จริง
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        print("Uploads folder created.")
        
    # สร้างโฟลเดอร์แบบอักษรหากไม่มีอยู่จริง
    if not os.path.exists('static/fonts'):
        os.makedirs('static/fonts')
        print("Static fonts folder created. Please add Sarabun-Regular.ttf and Sarabun-Bold.ttf")

if __name__ == '__main__':
    # สำหรับการพัฒนา local
    app.run(debug=True, host='127.0.0.1', port=5000)
else:
    # สำหรับ production deployment
    with app.app_context():
        db.create_all()
        # Initialize default settings if needed
        try:
            existing_setting = Settings.query.filter_by(key='header_note').first()
            if not existing_setting:
                default_setting = Settings(
                    key='header_note', 
                    value='(สำหรับบทความวิจัยที่ตีพิมพ์เผยแพร่หลังวันที่ 26 กันยายน พ.ศ. 2566)'
                )
                db.session.add(default_setting)
                db.session.commit()
        except Exception as e:
            db.session.rollback()