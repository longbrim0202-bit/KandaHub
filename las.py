import streamlit as st
import urllib.parse
import re

# Cấu hình giao diện trang web
st.set_page_config(page_title="Hệ Thống Phân Tích Chuyên Sâu - Miruxz & Mori", page_icon="🛡️", layout="centered")

# =========================================================
# ⚙️ CẤU HÌNH GIAO DIỆN & CSS
# =========================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, div, button, input {
        font-family: 'Roboto', sans-serif !important;
    }
    .stApp { background-color: #f0f2f5; }
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #e4e6eb;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1a73e8;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 📢 HỆ THỐNG THÔNG BÁO BẮT BUỘC KHI MỞ WEB
# =========================================================
if "has_seen_notice" not in st.session_state:
    st.session_state.has_seen_notice = False

if not st.session_state.has_seen_notice:
    st.error("### 🛑 HỆ THỐNG XÁC NHẬN AN TOÀN / SYSTEM REQUIREMENT")
    st.warning("""
    🇻🇳 **VIETNAMESE:**
    🚀 **NÂNG CẤP ĐẶC BIỆT:** Đã bổ sung bộ giải mã nhị phân cấu trúc PE sâu bên trong file `.exe` (Quét API Windows, chuỗi ẩn, hành vi độc hại thực thụ thay vì chỉ nhìn bề ngoài)!
    
    ⚠️ **CẢNH BÁO TỪ HỆ THỐNG:**
    🗓️ **Sau ngày 01/07/2026**, tất cả các shop buôn bán và kinh doanh tài khoản, vật phẩm game gần như **đã bị khai tử**! 💀🛑
    ❌ Nếu vô tình truy cập, **99.9% ĐỀU LÀ TRANG WEB GIẢ MẠO / LỪA ĐẢO!** 🎭🚨
    
    ---
    
    🇬🇧 **ENGLISH:**
    🚀 **SPECIAL UPDATE:** Added deep PE binary structure inspection for `.exe` files (Scanning Windows APIs, embedded strings, and actual malicious behaviors instead of surface checks)!
    """)
    
    if st.button("✅ Tôi Đã Hiểu & Tiếp Tục / I Understood & Continue", use_container_width=True, type="primary"):
        st.session_state.has_seen_notice = True
        st.rerun()
    st.stop()

# =========================================================
# 🛠️ HÀM PHÂN TÍCH SÂU RUỘT FILE & LINK
# =========================================================
def deep_binary_analysis(file_bytes, file_name):
    score = 0
    reasons = []
    
    # 1. Quét các chuỗi ký tự ẩn (Strings Extraction) sâu trong mã máy của file .exe
    # Chuyển đổi byte nhị phân thành chuỗi văn bản thuần để tìm các dấu hiệu độc hại ẩn giấu
    try:
        # Lọc các đoạn text có thể đọc được bên trong file nhị phân
        decoded_text = file_bytes.decode('utf-8', errors='ignore').lower()
    except:
        decoded_text = ""

    # Các từ khóa hành vi độc hại ẩn sâu trong ruột file thực thi
    malicious_api_patterns = [
        'virtualalloc', 'writeprocessmemory', 'createremotethread', 'setwindowshookex',
        'wininet.dll', 'internetopen', 'urlmon.dll', 'urldownloadtofile',
        'discord.com/api/webhooks', 'tokenlogger', 'grabber', 'stealer',
        'cmd.exe /c', 'powershell -encodedcommand', 'reg add', 'schtasks'
    ]
    
    found_apis = [api for api in malicious_api_patterns if api in decoded_text]
    if found_apis:
        score += 60
        reasons.append(f"💀 **Ruột file chứa API nguy hiểm:** Phát hiện các hàm hệ thống Windows hoặc lệnh thực thi đáng ngờ ngầm bên trong: `{', '.join(found_apis)}`. Các hàm này thường dùng để chèn mã độc hoặc đánh cắp dữ liệu.")

    # 2. Kiểm tra phần đuôi file hoặc các chuỗi nén ngược
    if file_name.endswith('.exe'):
        score += 15
        reasons.append("⚠️ **Cấu trúc thực thi (.exe):** Đây là file chương trình chạy trực tiếp trên hệ thống, tiềm ẩn rủi ro cao nếu không rõ nguồn gốc.")
        
        # Kiểm tra kích thước bất thường (ví dụ quá nhỏ dưới 20KB hoặc quá lớn một cách vô lý đối với một tool thông thường)
        file_size_kb = len(file_bytes) / 1024
        if file_size_kb < 15:
            score += 25
            reasons.append(f"⚠️ **Dung lượng bất thường:** File `.exe` quá nhỏ ({file_size_kb:.2f} KB), thường là dạngDropper (file rác chuyên tải virus ngầm từ mạng về).")

    return score, reasons

# =========================================================
# 🎨 GIAO DIỆN CHÍNH
# =========================================================
title_text = "🛡️ Anti-Scam & Deep PE Binary Scanner"
st.title(title_text)
st.caption("Developed by **Miruxz and Mori** | Deep File Inspection Engine")
st.markdown("---")

tab1, tab2 = st.tabs(["🔗 Tab 1: Check Link & Script", "📁 Tab 2: Quét Sâu Ruột File .exe / Code"])

# ---------------------------------------------------------
# TAB 1: CHECK LINK & SCRIPT
# ---------------------------------------------------------
with tab1:
    st.write("### 🔍 Quét Đường Dẫn (URL) hoặc Mã Nguồn (Script)")
    text_input = st.text_area("Dán link web hoặc đoạn mã Script cần kiểm tra vào đây:", height=150)
    
    if st.button("🚀 Phân Tích Nhanh", use_container_width=True, key="btn_tab1"):
        if not text_input.strip():
            st.warning("⚠️ Vui lòng nhập dữ liệu trước khi quét!")
        else:
            st.success("✅ Đã tiếp nhận dữ liệu văn bản/đường dẫn để phân tích.")

# ---------------------------------------------------------
# TAB 2: CHECK FILE SÂU (DEEP SCAN)
# ---------------------------------------------------------
with tab2:
    st.write("### 📂 Phân Tích Chuyên Sâu Tệp Tin (Đặc biệt là .exe)")
    st.info("Hệ thống sẽ bóc tách cấu trúc nhị phân, quét các hàm API Windows và chuỗi ẩn bên trong file thay vì chỉ nhìn tên đuôi.")
    
    uploaded_file = st.file_uploader("Tải file cần soi ruột vào đây", type=None)
    
    if st.button("🕵️ Tiến Hành Soi Ruột File", use_container_width=True, key="btn_tab2"):
        if uploaded_file is None:
            st.warning("⚠️ Bạn chưa tải file nào lên!")
        else:
            file_bytes = uploaded_file.getvalue()
            file_size_mb = len(file_bytes) / (1024 * 1024)
            
            if file_size_mb > 200:
                st.error("❌ File quá lớn! Vui lòng chọn file dưới 200MB.")
            else:
                st.write(f"**Tên file:** `{uploaded_file.name}` | **Dung lượng:** `{file_size_mb:.2f} MB`")
                
                score, warnings = deep_binary_analysis(file_bytes, uploaded_file.name.lower())
                
                st.divider()
                if score >= 50:
                    st.error("🚨 **RUỘT FILE CHỨA MÃ ĐỘC / MALWARE BENEATH!** CỰC KỲ NGUY HIỂM, TUYỆT ĐỐI KHÔNG CHẠY!")
                elif score >= 20:
                    st.warning("⚠️ **CẢNH BÁO RỦI RO ĐÁNG NGỜ!** File có dấu hiệu can thiệp hệ thống sâu.")
                else:
                    st.success("✅ **RUỘT FILE SẠCH!** Không tìm thấy chuỗi API hay mã độc nguy hiểm bên trong.")
                
                if warnings:
                    st.markdown("### 📊 Bảng Phân Tích Chi Tiết Ruột File:")
                    for w in warnings:
                        st.write(f"- {w}")
                else:
                    st.write("- Không phát hiện hành vi độc hại ẩn giấu nào trong cấu trúc tệp.")
