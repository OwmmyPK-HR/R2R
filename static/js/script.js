document.addEventListener('DOMContentLoaded', function() {

    // ==========================================================
    // === ส่วนที่ 1: การคำนวณอัตโนมัติทั้งหมดในฟอร์ม        ===
    // ==========================================================

    // --- Calculation for Section 3.3 ---
    const numInstitutesInput = document.getElementById('num_institutes_3_3');
    const shareAmountOutput = document.getElementById('share_amount_3_3');
    if (numInstitutesInput && shareAmountOutput) {
        numInstitutesInput.addEventListener('input', function() {
            const numInstitutes = parseInt(this.value, 10);
            if (numInstitutes > 0) {
                shareAmountOutput.value = (4000 / numInstitutes).toFixed(2);
            } else {
                shareAmountOutput.value = '';
            }
        });
    }

    // --- Calculation for Section 4.2 ---
    const intQuartileRadios = document.querySelectorAll('input[name="international_quartile"]');
    const shareIntBaseAmountInput = document.getElementById('share_int_base_amount');
    const shareIntNumInstitutesInput = document.getElementById('share_int_num_institutes');
    const shareIntFinalAmountOutput = document.getElementById('share_int_final_amount');
    if (intQuartileRadios.length > 0 && shareIntBaseAmountInput && shareIntNumInstitutesInput && shareIntFinalAmountOutput) {
        function calculateIntShare() {
            const baseAmount = parseFloat(shareIntBaseAmountInput.value) || 0;
            const numInstitutes = parseInt(shareIntNumInstitutesInput.value, 10) || 0;
            if (baseAmount > 0 && numInstitutes > 0) {
                shareIntFinalAmountOutput.value = (baseAmount / numInstitutes).toFixed(2);
            } else {
                shareIntFinalAmountOutput.value = '';
            }
        }
        intQuartileRadios.forEach(radio => radio.addEventListener('change', function() {
            if (this.checked) {
                shareIntBaseAmountInput.value = this.dataset.amount;
                calculateIntShare();
            }
        }));
        shareIntNumInstitutesInput.addEventListener('input', calculateIntShare);
    }

    // --- Calculation for Section 5.1 ---
    const specialNatNumInstitutesInput = document.getElementById('special_nat_share_num_institutes');
    const specialNatFinalAmountOutput = document.getElementById('special_nat_share_final_amount');
    if (specialNatNumInstitutesInput && specialNatFinalAmountOutput) {
        specialNatNumInstitutesInput.addEventListener('input', function() {
            const numInstitutes = parseInt(this.value, 10);
            if (numInstitutes > 0) {
                specialNatFinalAmountOutput.value = (1000 / numInstitutes).toFixed(2);
            } else {
                specialNatFinalAmountOutput.value = '';
            }
        });
    }

    // --- Calculation for Section 5.2 ---
    const specialIntQuartileRadios = document.querySelectorAll('input[name="special_international_quartile"]');
    const specialIntBaseAmountInput = document.getElementById('special_int_share_base_amount');
    const specialIntNumInstitutesInput = document.getElementById('special_int_share_num_institutes');
    const specialIntFinalAmountOutput = document.getElementById('special_int_share_final_amount');
    if (specialIntQuartileRadios.length > 0 && specialIntBaseAmountInput && specialIntNumInstitutesInput && specialIntFinalAmountOutput) {
        function calculateSpecialIntShare() {
            const baseAmount = parseFloat(specialIntBaseAmountInput.value) || 0;
            const numInstitutes = parseInt(specialIntNumInstitutesInput.value, 10) || 0;
            if (baseAmount > 0 && numInstitutes > 0) {
                specialIntFinalAmountOutput.value = (baseAmount / numInstitutes).toFixed(2);
            } else {
                specialIntFinalAmountOutput.value = '';
            }
        }
        specialIntQuartileRadios.forEach(radio => radio.addEventListener('change', function() {
            if (this.checked) {
                specialIntBaseAmountInput.value = this.dataset.amount;
                calculateSpecialIntShare();
            }
        }));
        specialIntNumInstitutesInput.addEventListener('input', calculateSpecialIntShare);
    }

    // --- Calculation for Section 6 ---
    const creativeCheckboxes = document.querySelectorAll('input[name^="creative_level_"]');
    const creativeBaseAmountInput = document.getElementById('creative_share_base_amount');
    const creativeNumInstitutesInput = document.getElementById('creative_share_num_institutes');
    const creativeFinalAmountOutput = document.getElementById('creative_share_final_amount');

// 2. ตรวจสอบให้แน่ใจว่า element ทั้งหมดมีอยู่จริง
if (creativeCheckboxes.length > 0 && creativeBaseAmountInput && creativeNumInstitutesInput && creativeFinalAmountOutput) {

    // 3. ฟังก์ชันสำหรับคำนวณการหาร (เหมือนเดิม)
    function calculateCreativeShare() {
        const baseAmount = parseFloat(creativeBaseAmountInput.value) || 0;
        const numInstitutes = parseInt(creativeNumInstitutesInput.value, 10) || 0;

        if (baseAmount > 0 && numInstitutes > 0) {
            const result = baseAmount / numInstitutes;
            creativeFinalAmountOutput.value = result.toFixed(2);
        } else {
            creativeFinalAmountOutput.value = '';
        }
    }
    // 4. ฟังก์ชัน สำหรับ "อัปเดตเงินฐาน" จาก "ผลรวม" ของ Checkbox ทั้งหมด
    function updateCreativeBaseAmount() {
        let totalAmount = 0;
        // วนลูปดู Checkbox ทุกอัน
        creativeCheckboxes.forEach(checkbox => {
            // ถ้าอันไหนถูกติ๊ก
            if (checkbox.checked) {
                // ให้บวกค่า data-amount เข้าไปในยอดรวม
                totalAmount += parseFloat(checkbox.dataset.amount) || 0;
            }
        });
        // อัปเดตค่าในช่อง "เงินฐาน"
        creativeBaseAmountInput.value = totalAmount;
        
        // เมื่อเงินฐานเปลี่ยน ให้คำนวณการหารใหม่ทันที
        calculateCreativeShare();
    }

    // 5. เพิ่ม Event Listener ให้กับ Checkbox ทุกอัน
    // เมื่อมีการ ติ๊ก/ยกเลิกติ๊ก ที่อันไหนก็ตาม ให้เรียกฟังก์ชันอัปเดตยอดรวม
    creativeCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateCreativeBaseAmount);
    });

    // 6. เพิ่ม Event Listener ให้กับช่องกรอกจำนวนสถาบัน (เหมือนเดิม)
    creativeNumInstitutesInput.addEventListener('input', calculateCreativeShare);
    }

    // ==========================================================
    // === ส่วนที่ 2: การทำงานอื่นๆ บนหน้าฟอร์มหลัก           ===
    // ==========================================================
    
    // --- ดึงชื่อผู้กรอกไปใส่ในหนังสือยินยอมอัตโนมัติ ---
    const mainApplicantNameInput = document.getElementById('fullName');
    const consentApplicantNameOutput = document.getElementById('consent_applicant_name');
    if (mainApplicantNameInput && consentApplicantNameOutput) {
        mainApplicantNameInput.addEventListener('input', function() {
            consentApplicantNameOutput.value = this.value;
        });
    }

    // --- แสดงชื่อไฟล์ที่เลือกสำหรับปุ่มอัปโหลด PDF ---
    const consentPdfInput = document.getElementById('consent_evidence_pdf');
    const consentPdfFilenameSpan = document.getElementById('consent_evidence_filename');
    if (consentPdfInput && consentPdfFilenameSpan) {
        consentPdfInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                consentPdfFilenameSpan.textContent = 'ไฟล์ที่เลือก: ' + this.files[0].name;
            } else {
                consentPdfFilenameSpan.textContent = '';
            }
        });
    }
    
    // --- ตรวจสอบเพดานตัวเลข 5,000 บาทสำหรับ Page charge (3.1) ---
    const pageChargeAmountInput = document.getElementById('page_charge_amount');
    if (pageChargeAmountInput) {
        pageChargeAmountInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value > 5000) {
                alert('จำนวนเงินต้องไม่เกิน 5,000 บาท ตามเพดานที่กำหนด');
                this.value = 5000; // ตั้งค่าเป็น 5000 อัตโนมัติ
            }
        });
        
        // ตรวจสอบเมื่อผู้ใช้พิมพ์เสร็จแล้ว (blur)
        pageChargeAmountInput.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (value > 5000) {
                alert('จำนวนเงินต้องไม่เกิน 5,000 บาท ตามเพดานที่กำหนด');
                this.value = 5000;
            }
        });
    }
    
    // --- ตรวจสอบเพดานตัวเลข 10,000 บาทสำหรับ International Page charge (4.1) ---
    const chargeIntAmountInput = document.getElementById('charge_int_amount');
    if (chargeIntAmountInput) {
        chargeIntAmountInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value > 10000) {
                alert('จำนวนเงินต้องไม่เกิน 10,000 บาท ตามเพดานที่กำหนด');
                this.value = 10000; // ตั้งค่าเป็น 10000 อัตโนมัติ
            }
        });
        
        // ตรวจสอบเมื่อผู้ใช้พิมพ์เสร็จแล้ว (blur)
        chargeIntAmountInput.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (value > 10000) {
                alert('จำนวนเงินต้องไม่เกิน 10,000 บาท ตามเพดานที่กำหนด');
                this.value = 10000;
            }
        });
    }
    
    // --- ตรวจสอบเพดานตัวเลข 10,000 บาทสำหรับ International Page charge Q1 Q2 (4.1.1) ---
    const chargeIntQ1Q2AmountInput = document.getElementById('charge_int_q1q2_amount');
    if (chargeIntQ1Q2AmountInput) {
        chargeIntQ1Q2AmountInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value > 10000) {
                alert('จำนวนเงินต้องไม่เกิน 10,000 บาท ตามเพดานที่กำหนด');
                this.value = 10000; // ตั้งค่าเป็น 10000 อัตโนมัติ
            }
        });
        
        // ตรวจสอบเมื่อผู้ใช้พิมพ์เสร็จแล้ว (blur)
        chargeIntQ1Q2AmountInput.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (value > 10000) {
                alert('จำนวนเงินต้องไม่เกิน 10,000 บาท ตามเพดานที่กำหนด');
                this.value = 10000;
            }
        });
    }
    
    // ==========================================================
    // === ส่วนที่ 3: ระบบ Popup ทั้งหมด (ส่งฟอร์ม, Login)  ===
    // ==========================================================

    // ฟังก์ชันตรวจสอบการติ๊กช่องสี่เหลี่ยมในแต่ละข้อ
    function validateCheckboxSections() {
        const sections = [
            {
                name: '1. คุณสมบัติของผู้ขอรับการสนับสนุนการตีพิมพบทความวิจัย',
                selectors: ['#qual_1_1', '#qual_1_2', '#qual_1_3']
            },
            {
                name: '2. ขอบเขตของบทความวิจัยหรืองานสร้างสรรค์ที่ขอรับการสนับสนุนค่าสมนาคุณ',
                selectors: ['#scope_2_1', '#scope_2_2', '#scope_2_3']  // ← เพิ่ม #scope_2_3
            },
            {
                name: '3. หลักเกณฑ์การจ่ายเงิน และรางวัลสนับสนุนการตีพิมพ์บทความวิจัย กรณีตีพิมพ์ในวารสารระดับชาติ',
                selectors: ['#payment_3_1', '#payment_3_2', '#payment_3_3']
            },
            {
                name: '4. หลักเกณฑ์การจ่ายเงิน และรางวัลสนับสนุนการตีพิมพ์บทความวิจัย กรณีตีพิมพ์ในวารสารระดับนานาชาติ',
                selectors: ['#charge_int_checkbox', '#charge_int_q1q2_checkbox', '#remuneration_int_checkbox', '#share_int_checkbox']
            },
            {
                name: '5. กรณีตีพิมพ์ในวารสาร ประเภทบทความวิจัยที่ถูกคัดเลือกมาจากการประชุมวิชาการและนำมาตีพิมพ์ลงใน วารสาร (Journal) และเป็นฉบับพิเศษ (Special Issue)',
                selectors: ['#special_nat_checkbox', '#special_nat_share_checkbox', '#special_int_checkbox', '#special_int_share_checkbox']
            },
            {
                name: '6. ค่าสมนาคุณงานสร้างสรรค์ที่เผยแพร่ แบ่งเป็น 5 ระดับ',
                selectors: ['#creative_level_asean', '#creative_level_inter_coop', '#creative_level_national', '#creative_level_institutional', '#creative_level_public', '#creative_share_checkbox']
            },
            {
                name: '7. หลักฐานประกอบการเสนอขอรับการสนับสนุน',
                selectors: ['input[name="evidence_page_charge_check"]', 'input[name="evidence_full_paper_check"]', 'input[name="evidence_consent_letter_check"]', 'input[name="evidence_quartile_check"]', 'input[name="evidence_tci_check"]', 'input[name="evidence_editorial_board_check"]', 'input[name="evidence_exhibition_check"]', 'input[name="evidence_proof_check"]', 'input[name="evidence_nrms_check"]', 'input[name="evidence_other_check"]']
            }
        ];

        for (let i = 0; i < sections.length; i++) {
            const section = sections[i];
            let hasChecked = false;
            
            for (let j = 0; j < section.selectors.length; j++) {
                const checkbox = document.querySelector(section.selectors[j]);
                if (checkbox && checkbox.checked) {
                    hasChecked = true;
                    break;
                }
            }
            
            if (!hasChecked) {
                return {
                    isValid: false,
                    message: `กรุณาเลือกอย่างน้อย 1 ข้อในส่วน "${section.name}" ก่อนส่งแบบฟอร์ม`
                };
            }
        }
        
        return { isValid: true };
    }

    // --- จัดการการส่งฟอร์มหลัก (Main Form Submission) ---
    const mainForm = document.getElementById('main-form');
    const successPopup = document.getElementById('popup-container');
    if (mainForm && successPopup) {
        const submitButton = mainForm.querySelector('button[type="submit"]');
        const popupTitle = successPopup.querySelector('#popup-title');
        const popupMessage = successPopup.querySelector('#popup-message');
        const popupClose = successPopup.querySelector('#popup-close');
        const popupContent = successPopup.querySelector('.popup-content');

        mainForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // ตรวจสอบการติ๊กช่องสี่เหลี่ยมในแต่ละข้อ
            const validationResult = validateCheckboxSections();
            if (!validationResult.isValid) {
                popupContent.classList.add('error');
                popupTitle.textContent = 'กรุณาตรวจสอบข้อมูล';
                popupMessage.textContent = validationResult.message;
                successPopup.style.display = 'flex';
                return;
            }
            
            submitButton.textContent = 'กำลังส่งข้อมูล...';
            submitButton.disabled = true;
            
            const formData = new FormData(mainForm);

            fetch('/', { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    popupContent.classList.remove('error');
                    popupTitle.textContent = 'สำเร็จ!';
                    popupMessage.textContent = data.message;
                    successPopup.style.display = 'flex';
                    mainForm.reset();
                    window.scrollTo(0, 0);
                } else {
                    popupContent.classList.add('error');
                    popupTitle.textContent = 'เกิดข้อผิดพลาด!';
                    popupMessage.textContent = data.message;
                    successPopup.style.display = 'flex';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                popupContent.classList.add('error');
                popupTitle.textContent = 'ผิดพลาดรุนแรง!';
                popupMessage.textContent = 'ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้';
                successPopup.style.display = 'flex';
            })
            .finally(() => {
                submitButton.textContent = 'ส่งข้อมูลทั้งหมด';
                submitButton.disabled = false;
            });
        });
        
        popupClose.addEventListener('click', () => { successPopup.style.display = 'none'; });
        // ลบ event listener สำหรับคลิกนอก popup
    }

    // --- จัดการ Popup Login ---
    const adminLoginBtn = document.getElementById('admin-login-btn');
    const loginPopupContainer = document.getElementById('login-popup-container');
    if (adminLoginBtn && loginPopupContainer) {
        const loginPopupClose = loginPopupContainer.querySelector('#login-popup-close');
        const loginForm = loginPopupContainer.querySelector('#login-form');
        const loginErrorMsg = loginPopupContainer.querySelector('#login-error-msg');

        adminLoginBtn.addEventListener('click', () => {
            loginPopupContainer.style.display = 'flex';
            if(loginErrorMsg) loginErrorMsg.textContent = '';
        });

        loginPopupClose.addEventListener('click', () => { loginPopupContainer.style.display = 'none'; });
        // ลบ event listener สำหรับคลิกนอก popup

        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(loginForm);

            fetch('/login', { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.href = data.redirect_url;
                } else {
                    if(loginErrorMsg) loginErrorMsg.textContent = data.message;
                }
            })
            .catch(error => {
                console.error('Login Error:', error);
                if(loginErrorMsg) loginErrorMsg.textContent = 'เกิดข้อผิดพลาดในการเชื่อมต่อ';
            });
        });
    }

   
    // ==========================================================
    // === ส่วนที่ 4: ระบบ Modal Popup ในหน้า Admin           ===
    // ==========================================================
    const detailsModal = document.getElementById('details-modal');
    if (detailsModal) {
        const modalBody = detailsModal.querySelector('#modal-body');
        const closeModalBtn = detailsModal.querySelector('.modal-close');
        const viewDetailsBtns = document.querySelectorAll('.view-details-btn');

        function openModal() { detailsModal.style.display = 'flex'; }
        function closeModal() { detailsModal.style.display = 'none'; }

        viewDetailsBtns.forEach(button => {
            button.addEventListener('click', function() {
                const submissionId = this.dataset.id;
                modalBody.innerHTML = '<p class="loading-text">กำลังโหลดข้อมูล...</p>';
                openModal();

                fetch(`/submission/${submissionId}`)
                .then(response => response.json())
                .then(data => {
                    if(data.error) {
                        modalBody.innerHTML = `<p style="color:red;">เกิดข้อผิดพลาด: ${data.error}</p>`;
                        return;
                    }
                    
                    let filesHtml = '<h3><i class="fas fa-folder-open"></i> ไฟล์ที่แนบมา</h3><ul class="file-list">';
                    let hasFiles = false;
                    const fileFields = [
                        { key: 'evidence_page_charge_upload', label: '7.1 หลักฐาน Page charge' }, { key: 'evidence_full_paper_upload', label: '7.2 สำเนา Full Paper' },
                        { key: 'evidence_consent_letter_upload', label: '7.3 หนังสือยินยอม' }, { key: 'evidence_quartile_upload', label: '7.4 หลักฐานค่าควอไทล์' },
                        { key: 'evidence_tci_upload', label: '7.5 หลักฐาน TCI' }, { key: 'evidence_editorial_board_upload', label: '7.6 รายชื่อกองบรรณาธิการ' },
                        { key: 'evidence_exhibition_upload', label: '7.7 สูจิบัตร' }, { key: 'evidence_proof_upload', label: '7.8 หลักฐานการเผยแพร่' },
                        { key: 'evidence_nrms_upload', label: '7.9 เอกสาร NRMS/DRMS' }, { key: 'evidence_other_upload', label: '7.10 เอกสารอื่นๆ' },
                        { key: 'applicant_signature_upload', label: 'ลายมือชื่อผู้ขอฯ' }, { key: 'dean_signature_upload', label: 'ลายมือชื่อคณบดี' },
                        { key: 'consent_evidence_pdf', label: 'หลักฐานเพิ่มเติม (หนังสือยินยอม)' },
                    ];
                    fileFields.forEach(field => {
                        if (data[field.key]) {
                            hasFiles = true;
                            filesHtml += `<li><a href="/uploads/${data[field.key]}" target="_blank"><i class="fas fa-file-pdf"></i> ${field.label}</a></li>`;
                        }
                    });
                    if (!hasFiles) { filesHtml += '<li>ไม่มีไฟล์แนบ</li>'; }
                    filesHtml += '</ul>';

                    modalBody.innerHTML = `<p><strong>ID:</strong> ${data.id}</p><p><strong>ชื่อผู้ส่ง:</strong> ${data.full_name || '-'}</p><p><strong>ตำแหน่ง:</strong> ${data.academic_position || '-'}</p><p><strong>สังกัด:</strong> ${data.affiliation || '-'}</p><hr>${filesHtml}`;
                })
                .catch(err => {
                    console.error("Fetch Error:", err);
                    modalBody.innerHTML = `<p style="color:red;">ไม่สามารถโหลดข้อมูลได้</p>`;
                });
            });
        });
        
        closeModalBtn.addEventListener('click', closeModal);
        // ลบ event listener สำหรับคลิกนอก modal
    }
    
});