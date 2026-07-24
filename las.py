import streamlit as st
import urllib.parse
import re

# Cấu hình giao diện trang web
st.set_page_config(page_title="Check Link Tự Động", page_icon="🛡️")

# =========================================================
# ⚙️ CẤU HÌNH GIAO DIỆN & PHÔNG NỀN
# =========================================================
FONT_NAME = "Roboto"
# =========================================================

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
# 📢 THÔNG BÁO QUAN TRỌNG KHI VỪA VÀO WEB
# =========================================================
@st.dialog("📢 THÔNG BÁO QUAN TRỌNG 📢")
def show_welcome_notice():
    st.warning("""
    ⚠️ **CẢNH BÁO TỪ HỆ THỐNG:**
    
    🗓️ **Sau ngày 01/07/2026**, tất cả các shop buôn bán và kinh doanh acc, vật phẩm game, đơn vị tiền ảo *(liên quan đến game)* gần như **đã bị khai tử**! 💀🛑
    
    ❌ Nếu mọi người có vô tình truy cập vào bất kỳ trang web nào có dịch vụ liên quan như trên thì **gần như 99.9% ĐỀU LÀ TRANG WEB GIẢ MẠO / LỪA ĐẢO!** 🎭🚨
    
    👉 Hãy cực kỳ cẩn trọng để tránh bị mất tiền và lộ thông tin cá nhân nhé! 🛡️✨
    """)
    if st.button("Đã Hiểu & Tiếp Tục 🚀", use_container_width=True):
        st.rerun()

if "has_seen_notice" not in st.session_state:
    st.session_state.has_seen_notice = True
    show_welcome_notice()

st.error("""
🚨 **CẢNH BÁO TỰ ĐỘNG (01/07/2026):** Sau thời điểm này, các shop kinh doanh acc/vật phẩm/tiền game gần như **đã bị khai tử** 💀. Bất kỳ web nào còn hoạt động dịch vụ trên đều có rủi ro cao là **GIẢ MẠO / LỪA ĐẢO**! ❌
""")

st.markdown("---")

# =========================================================
# GIAO DIỆN CHÍNH: KIỂM TRA ĐƯỜNG LINK (URL)
# =========================================================
st.title("🛡️Check Link/URL(BY MIRUXZ AND MORI)")
st.write("Dán đường dẫn (URL) vào bên dưới để hệ thống quét, phân tích độ an toàn và tra cứu thông tin nền tảng:")

url_input = st.text_input("", placeholder="Ví dụ: https://facebook.com hoặc link tải file bậy bạ...", label_visibility="collapsed")

def analyze_url(url):
    score = 0
    reasons = []
    safe_evidences = []
    web_info = None
    url_lower = url.lower()
    
    if not url_lower.startswith("https://"):
        score += 20
        reasons.append("⚠️ Web không có HTTPS (chỉ dùng HTTP, dễ bị chặn hoặc rò rỉ dữ liệu).")
    else:
        safe_evidences.append("🔒 **Giao thức kết nối an toàn (HTTPS):** Đường truyền được mã hóa bảo mật.")

    try:
        parsed = urllib.parse.urlparse(url if "://" in url else "http://" + url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        if not domain or "." not in domain:
            raise ValueError("Invalid domain")
    except:
        return 100, ["🚨 Định dạng đường dẫn bị lỗi!"], [], None

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

    # Kho lưu trữ thông tin các trang web chính hãng lớn
    official_database = {
        'facebook.com': {
            'name': '📘 Facebook (Meta)',
            'desc': 'Mạng xã hội lớn nhất toàn cầu do Meta phát triển, dùng để kết nối bạn bè, chia sẻ thông tin và giải trí.'
        },
        'google.com': {
            'name': '🔍 Google Search',
            'desc': 'Công cụ tìm kiếm thông tin lớn nhất thế giới, cung cấp các dịch vụ đám mây, bản đồ, email...'
        },
        'garena.vn': {
            'name': '🎮 Garena Việt Nam',
            'desc': 'Nhà phát hành game trực tuyến lớn (Free Fire, Liên Quân Mobile, FIFA Online 4...) tại khu vực Đông Nam Á.'
        },
        'roblox.com': {
            'name': '🧱 Roblox Corporation',
            'desc': 'Nền tảng trò chơi trực tuyến cho phép người dùng lập trình và chơi các trò chơi do cộng đồng sáng tạo.'
        },
        'steampowered.com': {
            'name': '🎮 Steam (Valve)',
            'desc': 'Hệ thống phân phối trò chơi điện tử bản quyền trên máy tính lớn nhất thế giới.'
        },
        'tiktok.com': {
            'name': '🎵 TikTok (ByteDance)',
            'desc': 'Nền tảng video âm nhạc và mạng xã hội chia sẻ các video ngắn định dạng dọc.'
        }
    }

    matched_official = None
    for off_domain, info in official_database.items():
        if domain.endswith(off_domain):
            matched_official = info
            break

    if matched_official:
        safe_evidences.append(f"✅ **Xác thực chính chủ:** Tên miền thuộc sở hữu của tổ chức lớn uy tín.")
        web_info = matched_official

    # Kiểm tra web tải file / link bậy bạ
    shady_download_keywords = [
        'download-free', 'tai-mien-phi', 'crack', 'full-crack', 'keygen', 'patch', 
        'freedownload', 'tai-nhanh', 'up-load', 'file-upload', 'mega-file', 'zippy',
        'rom-download', 'mod-apk-free', 'hoan-kiem', 'xem-phim-mien-phi'
    ]
    found_shady = [kw for kw in shady_download_keywords if kw in url_lower or kw in path]
    shady_file_exts = ['.exe', '.apk', '.bat', '.cmd', '.scr', '.iso', '.msi']
    has_shady_ext = any(path.endswith(ext) for ext in shady_file_exts)

    if found_shady or has_shady_ext:
        score += 45
        reasons.append(f"📥 **CẢNH BÁO WEB TẢI FILE / LINK BẬY BẠ ĐỘC HẠI:** Phát hiện dấu hiệu chia sẻ file không rõ nguồn gốc hoặc kích thích tải file tự do. Các trang này thường đính kèm mã độc, quảng cáo lừa đảo hoặc chuyển hướng độc hại!")

    # Bộ lọc hack/cheat
    cheat_keywords = ['hack', 'cheat', 'modmenu', 'mod-menu', 'script', 'delta', 'fluxus', 'aimbot', 'wallhack', 'modgame', 'hackgame', 'modapk']
    found_cheat = [kw for kw in cheat_keywords if kw in url_lower]
    if found_cheat:
        score += 50
        reasons.append(f"🎮 **Dấu hiệu HACK / CHEAT / GIAN LẬN GAME:** Phát hiện từ khóa độc hại (`{', '.join(found_cheat)}`). Nguy cơ bị **Khóa tài khoản vĩnh viễn (BAN)** và dính mã độc trộm nick!")

    game_keywords = ['roblox', 'ff', 'freefire', 'lienquan', 'pubg', 'genshin', 'robux', 'bloxfruit']
    shop_keywords = ['shop', 'acc', 'nick', 'giare', 'random', 'banacc', 'muaacc', 'vongquay', 'kimcuong']
    has_game_or_shop = any(kw in url_lower for kw in game_keywords + shop_keywords)

    if has_game_or_shop:
        score += 50
        reasons.append("🚨 **CẢNH BÁO SHOP GAME GIẢ MẠO (QUY ĐỊNH 01/07/2026):** Sau mốc 01/07/2026, hầu hết shop game đều đã bị khai tử. Web này có rủi ro rất cao là **GIẢ MẠO / LỪA ĐẢO**!")

    if score >= 50:
        reasons.append("🤣 **Cảnh báo: Link này nguy hiểm lắm, nhấn vào sẽ chặt tay! 🪓😜**")

    return score, reasons, safe_evidences, web_info

if st.button("🔍 Kiểm Tra Link Ngay", use_container_width=True):
    if not url_input.strip():
        st.warning("⚠️ Vui lòng dán link cần kiểm tra!")
    else:
        risk_score, warnings, evidences, info = analyze_url(url_input)
        st.divider()
        
        if info:
            st.info(f"📋 **HỒ SƠ NHẬN DIỆN THƯƠNG HIỆU:**\n\n- **Tên nền tảng:** {info['name']}\n- **Mô tả:** {info['desc']}")
            st.markdown("---")

        if risk_score >= 50:
            st.error("🚨 **CẢNH BÁO: LINK RẤT NGUY HIỂM / LỪA ĐẢO!**")
            for w in warnings:
                st.write(f"- {w}")
        elif risk_score >= 20:
            st.warning("⚠️ **CẢNH BÁO: LINK CÓ DẤU HIỆU NGHI VẤN!**")
            for w in warnings:
                st.write(f"- {w}")
        else:
            st.success("✅ **LINK CÓ VẺ AN TOÀN!**")
            st.write("📌 **Dẫn chứng an toàn:**")
            for e in evidences:
                st.write(f"- {e}")

# Dòng Note ghi chú ở cuối trang
st.markdown("---")
st.caption("📌 *(NOTE: Đây mới là phiên bản Beta và cũng là dự án đầu tay của chúng mình. Nếu có sai sót mong mọi người thông cảm và bỏ qua. Trong tương lai sẽ có những bản Mega update. Xin cảm ơn!)*")
