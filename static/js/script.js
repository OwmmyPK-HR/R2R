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
    // 4. ฟังก์ชันใหม่! สำหรับ "อัปเดตเงินฐาน" จาก "ผลรวม" ของ Checkbox ทั้งหมด
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
    
    // ==========================================================
    // === ส่วนที่ 3: ระบบ Popup ทั้งหมด (ส่งฟอร์ม, Login)  ===
    // ==========================================================

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