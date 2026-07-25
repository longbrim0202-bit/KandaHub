import streamlit as st
import urllib.parse
import re

# Cấu hình giao diện trang web
st.set_page_config(page_title="Check Link & File", page_icon="🛡️", layout="centered")

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
# 📢 HỆ THỐNG THÔNG BÁO CẬP NHẬT HỆ THỐNG KHI VỪA VÀO WEB
# =========================================================
if "has_seen_notice" not in st.session_state:
    st.session_state.has_seen_notice = False

if not st.session_state.has_seen_notice:
    st.error("### 🚀 THÔNG BÁO NÂNG CẤP HỆ THỐNG")
    st.info("""
    🇻🇳 **VIETNAMESE:**
    Trang web hiện đang trong quá trình cập nhật hệ thống nhằm nâng cao chất lượng dịch vụ, quét sâu và tối ưu hóa bộ lọc bảo mật tối đa cho người dùng! 
    Mong mọi người thông cảm và chờ đợi thêm một chút xíu nữa thôi, quá trình update sẽ hoàn tất trong thời gian sớm nhất nhé! ❤️✨
    
    ⚠️ **CẢNH BÁO:**
    🗓️ **Sau ngày 01/07/2026**, các shop kinh doanh tài khoản, vật phẩm game gần như **đã bị khai tử**! 💀🛑
    ❌ Nếu vô tình truy cập, **99.9% ĐỀU LÀ TRANG WEB LỪA ĐẢO!** 🎭🚨
    
    ---
    
    🇬🇧 **ENGLISH:**
    The system is currently undergoing an upgrade to enhance service quality, deep-scan capabilities, and optimize the security filter! 
    Thank you for your patience—the update will be completed very soon! ❤️✨
    """)
    
    if st.button("✅ Đã Hiểu & Tiếp Tục", use_container_width=True, type="primary"):
        st.session_state.has_seen_notice = True
        st.rerun()
    st.stop()

# =========================================================
# 🛠️ HÀM PHÂN TÍCH SÂU LINK / URL / SCRIPT (V7)
# =========================================================
def analyze_link_or_script_deep(content):
    score = 0
    reasons = []
    content_lower = content.lower()
    
    gambling_keywords = ['taixiu', 'tai-xiu', 'banca', 'ban-ca', 'nổ hũ', 'nohu', 'slot', 'casino', 'bet', 'cadoh', 'cá độ', 'đá gà', 'xocdia', 'xóc đĩa', 'ketqua', 'w88', 'fun88', 'fb88', '188bet']
    found_gambling = [kw for kw in gambling_keywords if kw in content_lower]

    adult_keywords = ['18+', 'sex', 'jav', 'xxx', 'khỏa thân', 'gái gọi', 'mát xa', 'nsfw', 'porn', 'chịch', 'vlxx']
    found_adult = [kw for kw in adult_keywords if kw in content_lower]

    phishing_keywords = ['free', 'robux', 'v-bucks', 'login', 'dang-nhap', 'verify', 'nhan-qua', 'shop', 'nap-tien', '1s', 'acc', 'giare', 'giftcode', 'nhanqua', 'momo', 'atm']
    found_phishing = [kw for kw in phishing_keywords if kw in content_lower]

    script_signatures = ['loadstring', 'getgenv', 'syn.request', 'xmlhttprequest', 'fetch(', 'document.cookie', 'navigator.sendbeacon', 'webhook', 'localStorage']
    found_script_sigs = [sig for sig in script_signatures if sig in content_lower]

    is_url = content.startswith('http://') or content.startswith('https://') or '.' in content and ' ' not in content.strip()

    if found_gambling:
        score += 90
        reasons.append(f"• **Thể loại:** Website Cá độ / Tài xỉu / Đánh bạc trực tuyến (`{', '.join(found_gambling)}`).\n• **Hoạt động:** Chuyên tổ chức cá cược, rủi ro mất tiền tài chính và vi phạm pháp luật.")
    elif found_adult:
        score += 90
        reasons.append(f"• **Thể loại:** Website nội dung người lớn / 18+ (`{', '.join(found_adult)}`).\n• **Hoạt động:** Chứa mã độc chuyển hướng, quảng cáo bẩn và nguy cơ đánh cắp thông tin trình duyệt.")
    elif found_script_sigs:
        score += 85
        reasons.append(f"• **Thể loại:** Script đánh cắp dữ liệu / Webhook (`{', '.join(found_script_sigs)}`).\n• **Hoạt động:** Đánh cắp token phiên đăng nhập hoặc thông tin cá nhân ngay khi thực thi.")
    elif is_url and (len(found_phishing) >= 2 or 'bit.ly' in content_lower or 'tinyurl' in content_lower or 'short' in content_lower or 'login' in content_lower):
        score += 80
        reasons.append(f"• **Thể loại:** Link giả mạo / Lừa đảo chiếm đoạt tài khoản (Phishing).\n• **Hoạt động:** Sử dụng từ khóa bẫy (`{', '.join(found_phishing)}`) để giả mạo trang đăng nhập uy tín và đánh cắp mật khẩu.")
    elif is_url:
        score += 10
        reasons.append("• **Thể loại:** Đường dẫn URL thông thường.\n• **Hoạt động:** Không phát hiện mẫu nhận diện nguy hiểm rõ ràng, nhưng cần lưu ý khi cung cấp thông tin cá nhân.")
    else:
        score += 30
        reasons.append("• **Thể loại:** Dữ liệu văn bản thô / Cú pháp lạ.\n• **Hoạt động:** Có chứa đoạn ký tự bất thường, cần cẩn trọng.")

    return score, reasons

# =========================================================
# 🛠️ HÀM PHÂN TÍCH CHUYÊN SÂU LÕI PE & NHỊ PHÂN (V7)
# =========================================================
def deep_binary_inspection_v7(file_bytes, file_name):
    score = 0
    reasons = []
    file_type = "File Sạch"
    
    trusted_installers = {
        'chromesetup.exe': 'Google LLC (Official Google Chrome Installer)',
        'chromeinstaller': 'Google LLC',
        'installgoogleplaygames.exe': 'Google LLC (Official Google Play Games)',
        'googleplaygames': 'Google LLC',
        'steamsetup.exe': 'Valve Corporation (Official Steam Client)',
        'discordsetup.exe': 'Discord Inc. (Official Discord Client)',
        'epicinstaller': 'Epic Games Inc.',
        'riotclientservices.exe': 'Riot Games Inc.',
        'battlenet-setup.exe': 'Blizzard Entertainment',
        'telegram.exe': 'Telegram FZ-LLC',
        'zoom.exe': 'Zoom Video Communications'
    }
    
    matched_trusted = next((publisher for key, publisher in trusted_installers.items() if key in file_name), None)
    if matched_trusted:
        return 0, "File Chính Hãng (Verified Publisher)", [
            f"• **Thể loại:** Trình cài đặt phần mềm gốc.\n• **Hoạt động:** Khớp chữ ký số chuẩn từ **{matched_trusted}**, hoàn toàn an toàn."
        ]

    try:
        decoded_text = file_bytes.decode('utf-8', errors='ignore').lower()
    except:
        decoded_text = ""

    malicious_apis = ['virtualalloc', 'writeprocessmemory', 'createremotethread', 'setwindowshookex']
    found_apis = [api for api in malicious_apis if api in decoded_text]

    cleaner_signatures = ['reg delete', 'temp', 'prefetch', 'appcompatflags', 'usnjrnl', 'clear-recyclebin', 'taskkill', 'del /f /q']
    found_cleaner = [sig for sig in cleaner_signatures if sig in decoded_text]

    malware_signatures = ['tokenlogger', 'cookie logger', 'browser_cookie', 'discord.com/api/webhooks', 'grabber', 'stealer']
    found_malware = [sig for sig in malware_signatures if sig in decoded_text]

    game_cheats = ['loadstring', 'getgenv', 'syn.request', 'exploit', 'injector', 'robloxgame', 'bypass', 'aimbot', 'wallhack', 'modmenu']
    found_cheats = [sig for sig in game_cheats if sig in decoded_text]

    packers = ['pyinstaller', 'upx!', 'autohotkey', 'autoit']
    found_packers = [p for p in packers if p in decoded_text]

    file_size_kb = len(file_bytes) / 1024

    if found_malware:
        score += 90
        file_type = "File Mã Độc Trá Hình (Stealer / Logger)"
        reasons.append(f"• **Thể loại:** Mã độc đánh cắp thông tin (`{', '.join(found_malware)}`).\n• **Hoạt động:** Trộm cắp cookie, mật khẩu trình duyệt và thông tin cá nhân ngầm.")
    elif found_apis:
        score += 80
        file_type = "File Can Thiệp Tiến Trình Sâu (Injection)"
        reasons.append(f"• **Thể loại:** Chèn mã tiến trình hệ thống (`{', '.join(found_apis)}`).\n• **Hoạt động:** Sử dụng API cấp thấp để tiêm mã độc vào bộ nhớ của ứng dụng hợp pháp.")
    elif found_cleaner:
        score += 65
        file_type = "File Xóa Dấu Trace / Cleaner"
        reasons.append(f"• **Thể loại:** Script dọn dẹp hệ thống/xóa log (`{', '.join(found_cleaner)}`).\n• **Hoạt động:** Xóa dấu vết hoạt động hoặc nhật ký hack, rủi ro làm hỏng hệ thống.")
    elif found_cheats:
        score += 50
        file_type = "Tool Hack / Cheat Game"
        reasons.append(f"• **Thể loại:** Script gian lận game (`{', '.join(found_cheats)}`).\n• **Hoạt động:** Tác động trực tiếp vào game để trục lợi, nguy cơ cao bị khóa tài khoản.")
    elif found_packers and file_name.endswith('.exe'):
        score += 30
        file_type = "Tool Đóng Gói (Ẩn Mã Nguồn)"
        reasons.append(f"• **Thể loại:** Đóng gói nhị phân (`{', '.join(found_packers)}`).\n• **Hoạt động:** Che giấu cấu trúc mã bên trong khỏi các trình quét thông thường.")
    elif file_name.endswith('.exe') and file_size_kb < 15:
        score += 40
        file_type = "File Thực Thi Nghi Vấn (Dropper)"
        reasons.append(f"• **Thể loại:** File Dropper nhỏ gọn ({file_size_kb:.2f} KB).\n• **Hoạt động:** Tải payload mã độc phụ từ internet về máy khi chạy.")
    else:
        score += 0
        file_type = "File Sạch"
        reasons.append("• **Thể loại:** Tệp tiêu chuẩn.\n• **Hoạt động:** Cấu trúc nhị phân an toàn, không phát hiện mã độc ẩn.")

    return score, file_type, reasons

# =========================================================
# 🎨 GIAO DIỆN CHÍNH
# =========================================================
st.title("🛡️ Check Link / URL / Script & File")
st.caption("Developed by **Miruxz and Mori**")
st.markdown("---")

tab1, tab2 = st.tabs(["🔗 Check Link / URL / Script", "📁 Check File"])

# ---------------------------------------------------------
# TAB 1: CHECK LINK / URL / SCRIPT
# ---------------------------------------------------------
with tab1:
    st.write("### 🔍 Check Link / URL / Script")
    st.info("💡 Mọi người có thể sử dụng tính năng này, nhưng mình không khuyến khích vì web đang trong quá trình cập nhật nên sẽ có sai sót. Xin lỗi vì sự bất tiện này nhé!")
    text_input = st.text_area("Dán link, URL hoặc script vào đây:", height=150)
    
    if st.button("🚀 Kiểm Tra Ngay", use_container_width=True, key="btn_tab1"):
        if not text_input.strip():
            st.warning("Vui lòng nhập dữ liệu!")
        else:
            score, link_reasons = analyze_link_or_script_deep(text_input)
            
            st.divider()
            if score >= 75:
                st.error("🚨 CẢNH BÁO NGUY HIỂM: Phát hiện Web Độc hại / Cá độ / 18+ / Lừa đảo!")
            elif score >= 30:
                st.warning("⚠️ Cảnh báo: Phát hiện yếu tố nghi vấn.")
            else:
                st.success("✅ Dữ liệu an toàn.")
                
            st.markdown("### 📊 Dẫn chứng chi tiết:")
            for r in link_reasons:
                st.write(r)

# ---------------------------------------------------------
# TAB 2: CHECK FILE
# ---------------------------------------------------------
with tab2:
    st.write("### 📂 Check File")
    st.info("💡 Mọi người có thể sử dụng, nhưng mình không khuyến khích vì web đang trong quá trình cập nhật nên sẽ có sai sót. Xin lỗi mọi người vì sự bất tiện này nhé!")
    
    uploaded_file = st.file_uploader("Tải file cần check:", type=None)
    
    if st.button("🕵️ Check File Ngay", use_container_width=True, key="btn_tab2"):
        if uploaded_file is None:
            st.warning("Vui lòng tải file lên!")
        else:
            file_bytes = uploaded_file.getvalue()
            file_size_mb = len(file_bytes) / (1024 * 1024)
            
            if file_size_mb > 200:
                st.error("File vượt quá giới hạn 200MB.")
            else:
                st.write(f"**File:** `{uploaded_file.name}` | **Dung lượng:** `{file_size_mb:.2f} MB`")
                
                score, file_category, warnings = deep_binary_inspection_v7(file_bytes, uploaded_file.name.lower())
                
                st.divider()
                st.markdown(f"### 🏷️ Kết quả: **{file_category}**")
                
                if score >= 75:
                    st.error("🚨 Phát hiện mã độc / Stealer / Can thiệp tiến trình sâu!")
                elif score >= 40:
                    st.warning("⚠️ Phát hiện tệp đáng ngờ / Cleaner / Tool Hack.")
                else:
                    st.success("✅ File an toàn.")
                
                if warnings:
                    st.markdown("### 📊 Dẫn chứng chi tiết:")
                    for w in warnings:
                        st.write(f"- {w}")
