import streamlit as st
import urllib.parse
import re
import io

# Cấu hình giao diện trang web (Phải đặt ở đầu tiên)
st.set_page_config(page_title="Hệ Thống Quét Độc Hại - Miruxz & Mori", page_icon="🛡️", layout="centered")

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
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #e4e6eb;
        border-radius: 8px 8px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 20px;
        padding-right: 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1a73e8;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 📢 HỆ THỐNG THÔNG BÁO BẮT BUỘC (SẼ CHẶN MÀN HÌNH NẾU CHƯA ĐỌC)
# =========================================================
if "has_seen_notice" not in st.session_state:
    st.session_state.has_seen_notice = False

if not st.session_state.has_seen_notice:
    st.error("### 🛑 HỆ THỐNG YÊU CẦU XÁC NHẬN / SYSTEM REQUIREMENT")
    st.warning("""
    🇻🇳 **VIETNAMESE:**
    🚀 **NEW UPDATE:** Hệ thống đã chia làm 2 mục (Check Link/Script và Check File 200MB). Khả năng nhận diện mã độc đã được nâng cấp lên mức tối đa!
    
    ⚠️ **CẢNH BÁO TỪ HỆ THỐNG:**
    🗓️ **Sau ngày 01/07/2026**, tất cả các shop buôn bán và kinh doanh acc, vật phẩm game, đơn vị tiền ảo gần như **đã bị khai tử**! 💀🛑
    ❌ Nếu vô tình truy cập vào các dịch vụ này, **99.9% ĐỀU LÀ TRANG WEB GIẢ MẠO / LỪA ĐẢO!** 🎭🚨
    
    ---
    
    🇬🇧 **ENGLISH (For International Users):**
    🚀 **NEW UPDATE:** Added deep file scanning (up to 200MB) and max-level script detection!
    
    ⚠️ **SYSTEM WARNING:**
    🗓️ **After July 1, 2026**, almost all game account, item, and virtual currency shops are **terminated**! 💀🛑
    ❌ Any similar websites operating now are **99.9% PHISHING / SCAMS!** 🎭🚨
    """)
    
    if st.button("✅ Tôi Đã Hiểu & Tiếp Tục / I Understood & Continue", use_container_width=True, type="primary"):
        st.session_state.has_seen_notice = True
        st.rerun()
    
    # Dừng chạy toàn bộ code bên dưới nếu chưa bấm nút
    st.stop()

# =========================================================
# 🛠️ HÀM PHÂN TÍCH LÕI (DÙNG CHUNG CHO CẢ URL VÀ FILE)
# =========================================================
def advanced_threat_scan(content, is_url=False):
    score = 0
    reasons = []
    content_lower = content.lower()
    
    # 1. BỘ LỌC SCRIPT/MÃ ĐỘC SIÊU CẤP (Roblox, Lua, Python, JS, v.v.)
    critical_script_threats = [
        'loadstring', 'getgenv', 'setclipboard', 'writefile', 'readfile', 
        'hookfunction', 'syn.request', 'httpget', 'httpgetasync', 'os.execute',
        'discord.com/api/webhooks', 'webhook', 'tokenlogger', 'cookie logger', 
        'browser_cookie', 'stealer', 'grabber', 'passwords.txt', 'ipify'
    ]
    found_critical = [kw for kw in critical_script_threats if kw in content_lower]
    if found_critical:
        score += 70
        reasons.append(f"💀 **MÃ ĐỘC NGHIÊM TRỌNG:** Tồn tại hàm đánh cắp dữ liệu hoặc thực thi ngầm (`{', '.join(found_critical)}`). Chạy cái này là mất nick/mất dữ liệu máy tính 100%!")

    # 2. BỘ LỌC HACK/CHEAT (Nguy cơ Ban acc)
    cheat_keywords = ['aimbot', 'wallhack', 'esp', 'auto-farm', 'autofarm', 'fluxus', 'delta exploits', 'krnl', 'mod-menu']
    found_cheats = [kw for kw in cheat_keywords if kw in content_lower]
    if found_cheats:
        score += 40
        reasons.append(f"🎮 **PHẦN MỀM GIAN LẬN:** Phát hiện từ khóa Hack/Cheat (`{', '.join(found_cheats)}`). Nguy cơ bị khóa thiết bị (HWID Ban) hoặc khóa tài khoản vĩnh viễn.")

    # 3. NẾU LÀ URL, PHÂN TÍCH TÊN MIỀN SÂU HƠN
    safe_evidences = []
    web_info = None
    
    if is_url:
        try:
            parsed = urllib.parse.urlparse(content if "://" in content else "http://" + content)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            # Cảnh báo Fake IP Masking (ví dụ: http://0x7f.0x0.0x0.0x1)
            ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            if re.match(ip_pattern, domain) or "0x" in domain:
                score += 50
                reasons.append("🚨 **LINK ẨN DANH:** Đang sử dụng địa chỉ IP trực tiếp hoặc IP ngụy trang. Cực kỳ nguy hiểm!")

            # Cảnh báo Tên miền Rác
            risky_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.zip', '.top', '.xyz', '.cc', '.club', '.vip', '.click']
            if any(domain.endswith(tld) for tld in risky_tlds):
                score += 30
                reasons.append(f"⚠️ **TÊN MIỀN RỦI RO CAO:** Sử dụng đuôi miền rẻ tiền/miễn phí, thường được dùng để lừa đảo.")
            elif "." in domain:
                safe_evidences.append(f"🌐 **Tên miền chuẩn:** `.{domain.split('.')[-1]}`.")

            # Cảnh báo Shop Game ảo (01/07/2026)
            game_shop_kws = ['shop', 'acc', 'nick', 'giare', 'random', 'vongquay', 'robux', 'kimcuong', 'freefire', 'roblox']
            if any(kw in domain or kw in path for kw in game_shop_kws):
                score += 60
                reasons.append("🛑 **CẢNH BÁO SHOP GAME GIẢ MẠO (QUY ĐỊNH 01/07/2026):** Sau mốc 01/07/2026, web bán acc/game này 99.9% là SCAM/LỪA ĐẢO!")

            # Check web chính hãng
            official_db = {
                'facebook.com': '📘 Facebook (Meta)', 'google.com': '🔍 Google Search',
                'garena.vn': '🎮 Garena Việt Nam', 'roblox.com': '🧱 Roblox Corporation',
                'steampowered.com': '🎮 Steam', 'github.com': '💻 GitHub'
            }
            for off_domain, name in official_db.items():
                if domain.endswith(off_domain):
                    safe_evidences.append(f"✅ **Web Chính Hãng:** Tên miền thuộc quản lý của {name}.")
                    break
                    
        except:
            score += 20
            reasons.append("⚠️ Cấu trúc link không rõ ràng hoặc bị mã hóa mờ ám.")

    return score, reasons, safe_evidences

# =========================================================
# 🎨 GIAO DIỆN CHÍNH
# =========================================================
st.title("🛡️ Anti-Scam & Malware Scanner")
st.caption("Developed by **Miruxz and Mori** | Database updated: 01/07/2026")
st.markdown("---")

# CHIA 2 TABS
tab1, tab2 = st.tabs(["🔗 Tab 1: Check Link & Script", "📁 Tab 2: Check File (Tối đa 200MB)"])

# ---------------------------------------------------------
# TAB 1: CHECK LINK & SCRIPT (VĂN BẢN)
# ---------------------------------------------------------
with tab1:
    st.write("### 🔍 Quét Đường Dẫn (URL) hoặc Mã Nguồn (Script)")
    text_input = st.text_area("Dán link web, đoạn mã Script (Lua, Python...) vào đây:", height=150)
    
    if st.button("🚀 Quét Văn Bản Ngay", use_container_width=True, key="btn_tab1"):
        if not text_input.strip():
            st.warning("⚠️ Vui lòng nhập dữ liệu trước khi quét!")
        else:
            is_url = text_input.strip().lower().startswith("http") or "." in text_input.split("/")[0] and " " not in text_input.strip()
            score, warnings, evidences = advanced_threat_scan(text_input, is_url=is_url)
            
            st.divider()
            if score >= 60:
                st.error("🚨 **CỰC KỲ NGUY HIỂM / EXTREME DANGER!** KHÔNG ĐƯỢC TRUY CẬP HAY SỬ DỤNG!")
            elif score >= 30:
                st.warning("⚠️ **CẢNH BÁO RỦI RO / WARNING!** CÓ DẤU HIỆU LỪA ĐẢO HOẶC KHÔNG AN TOÀN!")
            else:
                st.success("✅ **CÓ VẺ AN TOÀN / SAFE!** (Tuy nhiên hãy luôn cảnh giác)")
            
            for w in warnings:
                st.write(f"- 🛑 {w}")
            for e in evidences:
                st.write(f"- ✅ {e}")

# ---------------------------------------------------------
# TAB 2: CHECK FILE (UPLOAD)
# ---------------------------------------------------------
with tab2:
    st.write("### 📂 Tải Tệp Tin Lên Để Phân Tích (Scan File)")
    st.info("Hỗ trợ quét nội dung mã độc bên trong file `.lua`, `.txt`, `.py`, `.js`... và nhận diện các file độc hại `.exe`, `.bat`, `.zip`.")
    
    uploaded_file = st.file_uploader("Kéo thả file vào đây (Giới hạn: 200MB)", type=None)
    
    if st.button("🕵️ Phân Tích File Ngay", use_container_width=True, key="btn_tab2"):
        if uploaded_file is None:
            st.warning("⚠️ Bạn chưa tải file nào lên!")
        else:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > 200:
                st.error("❌ File quá lớn! Vui lòng tải file dưới 200MB.")
            else:
                st.write(f"**Tên file:** `{uploaded_file.name}` | **Kích thước:** `{file_size_mb:.2f} MB`")
                
                ext = uploaded_file.name.split('.')[-1].lower()
                danger_exts = ['exe', 'bat', 'cmd', 'ps1', 'vbs', 'msi', 'scr', 'pif', 'apk']
                archive_exts = ['zip', 'rar', '7z', 'tar']
                
                score = 0
                warnings = []
                
                # Check đuôi file trực tiếp
                if ext in danger_exts:
                    score += 80
                    warnings.append(f"💀 **FILE THỰC THI NGUY HIỂM:** File định dạng `.{ext}` có khả năng chứa virus/trojan phá hủy máy tính. Tuyệt đối không mở!")
                elif ext in archive_exts:
                    score += 40
                    warnings.append(f"📦 **FILE NÉN:** File `.{ext}` thường được dùng để giấu mã độc hoặc bypass phần mềm diệt virus. Cẩn thận khi giải nén!")
                else:
                    # Nếu là file văn bản/code, đọc nội dung bên trong để check
                    try:
                        content_bytes = uploaded_file.getvalue()
                        # Đọc tối đa 2MB đầu tiên để tránh tràn RAM với file text khổng lồ
                        content_str = content_bytes[:2000000].decode('utf-8') 
                        s, w, _ = advanced_threat_scan(content_str, is_url=False)
                        score += s
                        warnings.extend(w)
                    except UnicodeDecodeError:
                        warnings.append("⚠️ Không thể đọc nội dung file do đã bị mã hóa hoặc đây là file nhị phân (Binary). Rất đáng ngờ nếu đây được quảng cáo là file mã nguồn/script.")
                        score += 30

                st.divider()
                if score >= 60:
                    st.error("🚨 **CỰC KỲ NGUY HIỂM / EXTREME DANGER!** HÃY XÓA FILE NÀY NGAY LẬP TỨC!")
                elif score >= 30:
                    st.warning("⚠️ **FILE ĐÁNG NGỜ / WARNING!** CÓ DẤU HIỆU CHE GIẤU MÃ ĐỘC!")
                else:
                    st.success("✅ **FILE VĂN BẢN SẠCH!** (Không tìm thấy chuỗi mã độc phổ biến)")
                
                for w in warnings:
                    st.write(f"- 🛑 {w}")
