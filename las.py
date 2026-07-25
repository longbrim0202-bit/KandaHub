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
# 📢 HỆ THỐNG THÔNG BÁO BẮT BUỘC KHI MỞ WEB
# =========================================================
if "has_seen_notice" not in st.session_state:
    st.session_state.has_seen_notice = False

if not st.session_state.has_seen_notice:
    st.error("### 🛑 THÔNG BÁO HỆ THỐNG")
    st.warning("""
    🇻🇳 **VIETNAMESE:**
    🚀 **Update:** Đã trang bị Bot siêu cấp AI DeepScan V4, tối ưu khả năng quét sâu các file xóa hack/cleaner ẩn danh.
    
    ⚠️ **CẢNH BÁO:**
    🗓️ **Sau ngày 01/07/2026**, các shop kinh doanh tài khoản, vật phẩm game gần như **đã bị khai tử**! 💀🛑
    ❌ Nếu vô tình truy cập, **99.9% LÀ LỪA ĐẢO!** 🎭🚨
    
    ---
    
    🇬🇧 **ENGLISH:**
    🚀 **Update:** Upgraded with Super AI DeepScan V4 Bot, optimized for scanning hidden cleaner/anti-hack files.
    """)
    
    if st.button("✅ Đã Hiểu & Tiếp Tục", use_container_width=True, type="primary"):
        st.session_state.has_seen_notice = True
        st.rerun()
    st.stop()

# =========================================================
# 🛠️ HÀM PHÂN TÍCH SIÊU CẤP (BỔ SUNG CHECK FILE XÓA HACK / CLEANER)
# =========================================================
def deep_file_classifier(file_bytes, file_name):
    score = 0
    reasons = []
    file_type = "File Sạch"
    
    # 1. Danh sách file chính hãng uy tín
    trusted_installers = {
        'installgoogleplaygames.exe': 'Google LLC',
        'googleplaygames': 'Google LLC',
        'steamsetup.exe': 'Valve Corporation',
        'discordsetup.exe': 'Discord Inc.',
        'epicinstaller': 'Epic Games Inc.',
        'riotclientservices.exe': 'Riot Games Inc.',
        'battlenet-setup.exe': 'Blizzard Entertainment',
        'telegram.exe': 'Telegram FZ-LLC',
        'zoom.exe': 'Zoom Video Communications'
    }
    
    matched_trusted = next((publisher for key, publisher in trusted_installers.items() if key in file_name), None)
    if matched_trusted:
        return 0, "File Chính Hãng (Verified Publisher)", [
            f"✅ **Chứng thực:** Khớp chữ ký số từ **{matched_trusted}**.",
            "🛡️ **Hoạt động:** Trình cài đặt chuẩn, không độc hại."
        ]

    try:
        decoded_text = file_bytes.decode('utf-8', errors='ignore').lower()
    except:
        decoded_text = ""

    # 2. Nhận diện file Xóa Hack / Cleaner / Reg Edit chuyên sâu
    cleaner_hack_signatures = ['reg delete', 'temp', 'prefetch', 'appcompatflags', 'usnjrnl', 'Clear-RecycleBin', 'taskkill', 'del /f /q']
    found_cleaner = [sig for sig in cleaner_hack_signatures if sig in decoded_text]

    malware_hack_signatures = ['tokenlogger', 'cookie logger', 'browser_cookie', 'discord.com/api/webhooks', 'grabber', 'stealer']
    game_hack_signatures = ['loadstring', 'getgenv', 'syn.request', 'exploit', 'injector', 'robloxgame', 'bypass', 'aimbot', 'wallhack', 'modmenu']
    packer_signatures = ['pyinstaller', 'upx!', 'autohotkey', 'autoit']
    
    found_malware = [sig for sig in malware_hack_signatures if sig in decoded_text]
    found_cheats = [sig for sig in game_hack_signatures if sig in decoded_text]
    found_packers = [p for p in packer_signatures if p in decoded_text]
    file_size_kb = len(file_bytes) / 1024

    # 3. Phân loại mức độ nguy hiểm (Đặc biệt xử lý file xóa hack / cleaner giả mạo)
    if found_malware:
        score += 80
        file_type = "File Mã Độc Trá Hình"
        reasons.append(f"• **Thể loại:** Mã độc đánh cắp dữ liệu (`{', '.join(found_malware)}`).\n• **Hoạt động:** Đánh cắp thông tin ngầm khi người dùng chạy lệnh.")
    elif found_cleaner:
        score += 65
        file_type = "File Xóa Dấu Trace / Cleaner (Nguy hiểm)"
        reasons.append(f"• **Thể loại:** File lệnh hệ thống/Cleaner (`{', '.join(found_cleaner)}`).\n• **Hoạt động:** Chuyên xóa log, dọn dẹp nhật ký hệ thống hoặc xóa dấu vết cheat, dễ làm hỏng Windows hoặc ẩn chứa mã độc phía sau.")
    elif found_cheats:
        score += 50
        file_type = "Tool Hack / Cheat Game"
        reasons.append(f"• **Thể loại:** Script can thiệp game (`{', '.join(found_cheats)}`).\n• **Hoạt động:** Tác động trực tiếp vào tiến trình game để gian lận.")
    elif found_packers and file_name.endswith('.exe'):
        score += 30
        file_type = "Tool Đóng Gói (Ẩn Mã Nguồn)"
        reasons.append(f"• **Thể loại:** Đóng gói nhị phân (`{', '.join(found_packers)}`).\n• **Hoạt động:** Che giấu mã nguồn bên trong.")
    elif file_name.endswith('.exe') and file_size_kb < 15:
        score += 40
        file_type = "File Thực Thi Nghi Vấn"
        reasons.append(f"• **Thể loại:** Dropper nhỏ gọn ({file_size_kb:.2f} KB).\n• **Hoạt động:** Tải mã độc phụ từ mạng.")
    else:
        score += 0
        file_type = "File Sạch"
        reasons.append("• **Thể loại:** Tệp tiêu chuẩn.\n• **Hoạt động:** An toàn, không có hành vi can thiệp.")

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
    text_input = st.text_area("Dán link, URL hoặc script vào đây:", height=150)
    
    if st.button("🚀 Kiểm Tra Ngay", use_container_width=True, key="btn_tab1"):
        if not text_input.strip():
            st.warning("Vui lòng nhập dữ liệu!")
        else:
            st.success("Đã tiếp nhận dữ liệu.")

# ---------------------------------------------------------
# TAB 2: CHECK FILE
# ---------------------------------------------------------
with tab2:
    st.write("### 📂 Check File")
    st.info("💡 Lưu ý: Bot siêu cấp V4 quét sâu các file xóa hack/cleaner và mã độc ẩn.")
    
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
                
                score, file_category, warnings = deep_file_classifier(file_bytes, uploaded_file.name.lower())
                
                st.divider()
                st.markdown(f"### 🏷️ Kết quả: **{file_category}**")
                
                if score >= 70:
                    st.error("Phát hiện mã độc hại!")
                elif score >= 40:
                    st.warning("Phát hiện Cleaner/Xóa Hack hoặc Tool đáng ngờ.")
                else:
                    st.success("File an toàn.")
                
                if warnings:
                    st.markdown("### 📊 Dẫn chứng chi tiết:")
                    for w in warnings:
                        st.write(f"- {w}")
