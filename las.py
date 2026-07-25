import streamlit as st
import urllib.parse
import re

# Cấu hình giao diện trang web
st.set_page_config(page_title="Check Link & Script Tự Động", page_icon="🛡️")

# =========================================================
# ⚙️ CẤU HÌNH GIAO DIỆN & PHÔNG NỀN
# =========================================================
FONT_NAME = "Roboto"

# Áp dụng CSS giao diện
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family={FONT_NAME.replace(" ", "+")}:wght@400;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, p, div, button, input {{
        font-family: '{FONT_NAME}', sans-serif !important;
    }}

    .stApp {{
        background-color: #f0f2f5;
    }}

    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.93);
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 📢 THÔNG BÁO QUAN TRỌNG KHI VỪA VÀO WEB (CÓ UPDATE & ENG)
# =========================================================
@st.dialog("📢 THÔNG BÁO QUAN TRỌNG / IMPORTANT NOTICE 📢")
def show_welcome_notice():
    st.warning("""
    🇻🇳 **VIETNAMESE:**
    🚀 **NEW UPDATE:** Đã add thêm tính năng nhận diện script siêu cấp, tích hợp thêm tính năng check file cho mọi người nhé!
    
    ⚠️ **CẢNH BÁO TỪ HỆ THỐNG:**
    🗓️ **Sau ngày 01/07/2026**, tất cả các shop buôn bán và kinh doanh acc, vật phẩm game, đơn vị tiền ảo gần như **đã bị khai tử**! 💀🛑
    ❌ Nếu vô tình truy cập, **99.9% ĐỀU LÀ TRANG WEB GIẢ MẠO / LỪA ĐẢO!** 🎭🚨
    
    ---
    
    🇬🇧 **ENGLISH (For International Users):**
    🚀 **NEW UPDATE:** Added advanced script detection features and a file checking system for everyone!
    
    ⚠️ **SYSTEM WARNING:**
    🗓️ **After July 1, 2026**, almost all game account, item, and virtual currency shops are **terminated**! 💀🛑
    ❌ Any similar websites operating now are **99.9% PHISHING / SCAMS!** 🎭🚨
    """)
    if st.button("Đã Hiểu & Tiếp Tục / Understood & Continue 🚀", use_container_width=True):
        st.rerun()

if "has_seen_notice" not in st.session_state:
    st.session_state.has_seen_notice = True
    show_welcome_notice()

st.error("""
🚨 **CẢNH BÁO TỰ ĐỘNG (01/07/2026):** Sau thời điểm này, các shop kinh doanh acc/vật phẩm/tiền game gần như **đã bị khai tử** 💀. Bất kỳ web nào còn hoạt động dịch vụ trên đều có rủi ro cao là **GIẢ MẠO / LỪA ĐẢO**! ❌
""")

st.markdown("---")

# =========================================================
# GIAO DIỆN CHÍNH: KIỂM TRA ĐƯỜNG LINK & SCRIPT
# =========================================================
st.title("🛡️ Check Link/URL & Script (BY MIRUXZ AND MORI)")
st.write("Dán đường dẫn (URL) hoặc nội dung Script/Tên file cần kiểm tra vào bên dưới để hệ thống quét chuyên sâu:")

url_input = st.text_input("", placeholder="Ví dụ: Link web, nội dung script Roblox, hoặc tên file độc hại...", label_visibility="collapsed")

def analyze_input(user_input):
    score = 0
    reasons = []
    safe_evidences = []
    web_info = None
    input_lower = user_input.lower()
    
    # Kiểm tra xem đây có phải là nội dung Script hoặc đoạn mã độc hay không
    script_danger_keywords = [
        'loadstring', 'game:getservice', 'getgenv', 'fireclickdetector', 
        'httpget', 'getclipboard', 'syn.request', 'fluxus', 'delta', 
        'robloxgame', 'exploit', 'webhook', 'discord.com/api/webhooks', 
        'tokenlogger', 'cookie', 'steal', 'hack', 'cheat', 'aimbot', 'wallhack'
    ]
    
    found_script_threats = [kw for kw in script_danger_keywords if kw in input_lower]
    
    # Kiểm tra định dạng file độc hại
    shady_file_exts = ['.exe', '.apk', '.bat', '.cmd', '.scr', '.iso', '.msi', '.vbs', '.ps1', '.jar', '.rar', '.zip']
    has_shady_file = any(input_lower.endswith(ext) or ext + " " in input_lower for ext in shady_file_exts)

    if has_shady_file:
        score += 55
        reasons.append("📁 **CẢNH BÁO TỆP TIN / FILE ĐỘC HẠI:** Phát hiện định dạng file có rủi ro thực thi mã độc cao (như `.exe`, `.apk`, `.bat`, `.vbs`,...). Tuyệt đối không tải hoặc chạy file này nếu không rõ nguồn gốc!")

    if found_script_threats:
        score += 60
        reasons.append(f"📜⚠️ **CẢNH BÁO SCRIPT / MÃ ĐỘC NGUY HIỂM:** Phát hiện các hàm thực thi nguy hiểm hoặc từ khóa đáng ngờ (`{', '.join(found_script_threats)}`). Script này có nguy cơ chứa mã đánh cắp thông tin (Token/Cookie Logger) hoặc làm khóa tài khoản vĩnh viễn!")

    # Nếu input không bắt đầu bằng http nhưng có chứa dạng text script dài
    if not input_lower.startswith("http://") and not input_lower.startswith("https://"):
        if len(user_input) > 50 and not has_shady_file and not found_script_threats:
            score += 15
            reasons.append("🔍 **KIỂM TRA ĐOẠN VĂN BẢN/SCRIPT:** Đây không phải định dạng URL chuẩn. Hệ thống đã phân tích nhưng không tìm thấy chữ ký mã độc rõ ràng, tuy nhiên vẫn cần cẩn trọng với các đoạn code lạ.")
        elif not has_shady_file and not found_script_threats:
            # Xử lý như URL bình thường nếu ngắn
            pass

    if input_lower.startswith("http://") or input_lower.startswith("https://") or "." in user_input:
        try:
            parsed = urllib.parse.urlparse(user_input if "://" in user_input else "http://" + user_input)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            if not domain or "." not in domain:
                raise ValueError("Invalid domain")
        except:
            if score == 0:
                return 100, ["🚨 Định dạng đường dẫn hoặc cấu trúc dữ liệu bị lỗi!"], [], None
            else:
                return score, reasons, safe_evidences, None

        ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        if re.match(ip_pattern, domain):
            score += 40
            reasons.append("🚨 Sử dụng địa chỉ IP trực tiếp (Rủi ro lừa đảo rất cao!).")

        risky_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.zip', '.top', '.work', '.xyz', '.cc', '.club', '.vip', '.site', '.online']
        if any(domain.endswith(tld) for tld in risky_tlds):
            score += 25
            reasons.append("⚠️ Sử dụng đuôi tên miền rẻ/miễn phí có rủi ro cao (.xyz, .tk, .vip, .club...).")
        else:
            safe_evidences.append(f"🌐 **Sử dụng tên miền chuẩn/phổ biến:** `.{domain.split('.')[-1]}`.")

        official_database = {
            'facebook.com': {'name': '📘 Facebook (Meta)', 'desc': 'Mạng xã hội lớn nhất toàn cầu do Meta phát triển.'},
            'google.com': {'name': '🔍 Google Search', 'desc': 'Công cụ tìm kiếm thông tin lớn nhất thế giới.'},
            'garena.vn': {'name': '🎮 Garena Việt Nam', 'desc': 'Nhà phát hành game trực tuyến lớn tại khu vực ĐNÁ.'},
            'roblox.com': {'name': '🧱 Roblox Corporation', 'desc': 'Nền tảng trò chơi trực tuyến toàn cầu.'},
            'steampowered.com': {'name': '🎮 Steam (Valve)', 'desc': 'Hệ thống phân phối trò chơi điện tử bản quyền.'},
            'tiktok.com': {'name': '🎵 TikTok (ByteDance)', 'desc': 'Nền tảng video ngắn và mạng xã hội.'}
        }

        matched_official = None
        for off_domain, info in official_database.items():
            if domain.endswith(off_domain):
                matched_official = info
                break

        if matched_official:
            safe_evidences.append(f"✅ **Xác thực chính chủ:** Tên miền thuộc sở hữu của tổ chức lớn uy tín.")
            web_info = matched_official

        shady_download_keywords = ['download-free', 'tai-mien-phi', 'crack', 'full-crack', 'keygen', 'patch', 'freedownload', 'tai-nhanh', 'up-load', 'file-upload', 'mega-file', 'zippy']
        found_shady = [kw for kw in shady_download_keywords if kw in input_lower or kw in path]
        if found_shady:
            score += 45
            reasons.append(f"📥 **CẢNH BÁO WEB TẢI FILE ĐỘC HẠI:** Phát hiện dấu hiệu chia sẻ file không rõ nguồn gốc, dễ đính kèm mã độc!")

        game_keywords = ['roblox', 'ff', 'freefire', 'lienquan', 'pubg', 'genshin', 'robux', 'bloxfruit']
        shop_keywords = ['shop', 'acc', 'nick', 'giare', 'random', 'banacc', 'muaacc', 'vongquay', 'kimcuong']
        has_game_or_shop = any(kw in input_lower for kw in game_keywords + shop_keywords)

        if has_game_or_shop:
            score += 50
            reasons.append("🚨 **CẢNH BÁO SHOP GAME GIẢ MẠO (QUY ĐỊNH 01/07/2026):** Sau mốc 01/07/2026, hầu hết shop game đều đã bị khai tử. Web này có rủi ro rất cao là **GIẢ MẠO / LỪA ĐẢO**!")

    if score >= 50:
        reasons.append("🤣 **Cảnh báo: Dữ liệu này nguy hiểm lắm, nhấn vào hoặc chạy là bay màu tài khoản! 🪓😜**")

    return score, reasons, safe_evidences, web_info

if st.button("🔍 Kiểm Tra Ngay (Check Link & Script/File)", use_container_width=True):
    if not url_input.strip():
        st.warning("⚠️ Vui lòng dán đường dẫn, mã script hoặc tên file cần kiểm tra!")
    else:
        risk_score, warnings, evidences, info = analyze_input(url_input)
        st.divider()
        
        if info:
            st.info(f"📋 **HỒ SƠ NHẬN DIỆN THƯƠNG HIỆU:**\n\n- **Tên nền tảng:** {info['name']}\n- **Mô tả:** {info['desc']}")
            st.markdown("---")

        if risk_score >= 50:
            st.error("🚨 **CẢNH BÁO: DỮ LIỆU / SCRIPT / LINK NÀY RẤT NGUY HIỂM & ĐỘC HẠI!**")
            for w in warnings:
                st.write(f"- {w}")
        elif risk_score >= 20:
            st.warning("⚠️ **CẢNH BÁO: CÓ DẤU HIỆU NGHI VẤN / RỦI RO CAO!**")
            for w in warnings:
                st.write(f"- {w}")
        else:
            st.success("✅ **DỮ LIỆU / LINK CÓ VẺ AN TOÀN!**")
            if evidences:
                st.write("📌 **Dẫn chứng an toàn:**")
                for e in evidences:
                    st.write(f"- {e}")

# Dòng Note ghi chú ở cuối trang
st.markdown("---")
st.caption("📌 *(NOTE: Đây là phiên bản nâng cấp bổ sung bộ lọc kiểm tra Script và Check File chuyên sâu. Nếu có sai sót mong mọi người thông cảm. Xin cảm ơn!)*")
