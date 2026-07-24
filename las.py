import streamlit as st
import urllib.parse
import re

# Cấu hình giao diện trang web
st.set_page_config(page_title="Check Link Tự Động", page_icon="🛡️")

# =========================================================
# ⚙️ CẤU HÌNH GIAO DIỆN & PHÔNG NỀN
# =========================================================
BG_IMAGE_URL = "" 
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
        background-image: url("{BG_IMAGE_URL}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
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

# Kích hoạt popup thông báo lần đầu truy cập
if "has_seen_notice" not in st.session_state:
    st.session_state.has_seen_notice = True
    show_welcome_notice()

# Ban-nơ cảnh báo cố định ở đầu trang web để mọi người luôn đọc được
st.error("""
🚨 **CẢNH BÁO TỰ ĐỘNG (01/07/2026):** Sau thời điểm này, các shop kinh doanh acc/vật phẩm/tiền game gần như **đã bị khai tử** 💀. Bất kỳ web nào còn hoạt động dịch vụ trên đều có rủi ro cao là **GIẢ MẠO / LỪA ĐẢO**! ❌
""")

st.markdown("---")

# --- NỘI DUNG WEB ---
st.title("🛡️ Check Link/URL(By Miruxz and Mori)")
st.write("Dán đường dẫn (URL) vào bên dưới để hệ thống quét và phân tích độ an toàn:")

url_input = st.text_input("", placeholder="Ví dụ: https://facebook.com hoặc http://dangnhap-garena-nhankimcuong.xyz", label_visibility="collapsed")

def analyze_url(url):
    """Hàm phân tích độ uy tín của URL"""
    score = 0
    reasons = []
    safe_evidences = [] # Danh sách dẫn chứng an toàn
    url_lower = url.lower()
    
    # 1. Kiểm tra HTTPS
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
        return 100, ["🚨 Định dạng đường dẫn bị lỗi! 😂 Nhấn vào sẽ chặt tay! 🪓🤣"], []

    # 2. Kiểm tra nếu dùng IP trực tiếp
    ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    if re.match(ip_pattern, domain):
        score += 40
        reasons.append("🚨 Sử dụng địa chỉ IP trực tiếp (Rủi ro lừa đảo rất cao!).")

    # 3. Kiểm tra đuôi tên miền rẻ / rủi ro
    risky_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.zip', '.top', '.work', '.xyz', '.cc', '.club', '.vip', '.site', '.online']
    if any(domain.endswith(tld) for tld in risky_tlds):
        score += 25
        reasons.append("⚠️ Sử dụng đuôi tên miền rẻ/miễn phí có rủi ro cao (.xyz, .tk, .vip, .club...).")
    else:
        safe_evidences.append(f"🌐 **Sử dụng tên miền chuẩn/phổ biến:** `.{domain.split('.')[-1]}` (Không phải tên miền rác/rẻ tiền).")

    # Danh sách tên miền chính chủ chuẩn
    official_domains = [
        'facebook.com', 'google.com', 'garena.vn', 'steampowered.com', 
        'roblox.com', 'tiktok.com', 'zalo.me', 'momo.vn', 'apple.com', 'microsoft.com', 'youtube.com'
    ]
    is_official = any(domain.endswith(off) for off in official_domains)
    if is_official:
        safe_evidences.append(f"✅ **Thương hiệu chính chủ:** Nhận diện tên miền thuộc nền tảng lớn uy tín (`{domain}`).")

    # 4. Kiểm tra Dấu hiệu CÂU TÀI KHOẢN / ĐĂNG NHẬP LỪA ĐẢO (PHISHING)
    login_keywords = ['login', 'dangnhap', 'dang-nhap', 'signin', 'sign-in', 'account', 'verify', 'xacthuc', 'capnhat-taikhoan', 'khoa-taikhoan']
    target_platforms = ['facebook', 'fb', 'garena', 'google', 'gmail', 'steam', 'roblox', 'tiktok', 'zalo', 'momo', 'bank']
    
    found_login_kw = [kw for kw in login_keywords if kw in url_lower]
    found_target = [tp for tp in target_platforms if tp in url_lower]

    if found_login_kw and not is_official:
        score += 45
        reasons.append(f"🔑 **CẢNH BÁO ĐĂNG NHẬP VỚ VẨN / PHISHING:** Phát hiện trang yêu cầu đăng nhập/xác thực (`{', '.join(found_login_kw)}`) không thuộc web chính chủ. **TUYỆT ĐỐI KHÔNG** nhập mật khẩu, OTP hay tài khoản vào đây!")
    elif found_target and not is_official:
        score += 40
        reasons.append(f"🎭 **Dấu hiệu GIẢ MẠO NỀN TẢNG:** Web có chứa tên thương hiệu (`{', '.join(found_target)}`) nhưng tên miền không phải chính chủ. Dấu hiệu lừa đảo lấy nick!")

    # 5. Kiểm tra Dấu hiệu CÁ ĐỘ / TÀI XỈU / ĐÁNH BẠC
    gambling_keywords = [
        'taixiu', 'tai-xiu', 'xocdia', 'xoc-dia', 'bet', 'casino', 'cacuoc', 'nhacai', 
        'keonhacai', 'kubet', 'shbet', '88bet', 'fun88', 'w88', 'f8bet', 'jun88', 
        'hi88', 'baccarat', 'slot', 'gamebai', 'nohu', 'danhbac', 'kèo', 'sunwin', 'go88'
    ]
    found_gambling = [kw for kw in gambling_keywords if kw in url_lower]
    if found_gambling:
        score += 45
        reasons.append(f"🎰 **Dấu hiệu TÀI XỈU / CÁ ĐỘ / CỜ BẠC:** Chứa từ khóa nhà cái, tài xỉu (`{', '.join(found_gambling)}`). Rất dễ bị ngấm mã độc và mất tiền!")

    # 6. Kiểm tra Dấu hiệu BÓNG ĐÁ LẬU / XEM CHÙA
    pirate_football_keywords = [
        'xoilac', 'vebo', 'mitom', 'socolive', 'cakhia', 'rautuoc', '90phut', 
        'tiengruoi', 'truoctiepbongda', 'tructiepbongda', 'livebongda', 'linkbongda'
    ]
    found_football = [kw for kw in pirate_football_keywords if kw in url_lower]
    if found_football:
        score += 35
        reasons.append(f"⚽ **Dấu hiệu BÓNG ĐÁ LẬU:** Nhận diện web xem bóng đá chui (`{', '.join(found_football)}`). Các web này thường gài dày đặc quảng cáo cờ bạc, mã độc tự nhảy pop-up!")

    # 7. Kiểm tra Dấu hiệu WEB PHIM 18+ / ĐỒI TRỤY
    adult_keywords = [
        'porn', 'hentai', 'sex', '18plus', 'phim18', 'jav', 'vlxx', 'xnx', 
        'phimsex', 'lon', 'cuclip', 'clipnong', 'loncon', 'thang18'
    ]
    found_adult = [kw for kw in adult_keywords if kw in url_lower]
    if found_adult:
        score += 45
        reasons.append(f"🔞 **Dấu hiệu WEB PHIM 18+ / NỘI DUNG ĐỒI TRỤY:** Chứa từ khóa nhạy cảm (`{', '.join(found_adult)}`). Các trang này chứa mật độ virus và lừa đảo đánh cắp thông tin cá nhân cực kỳ cao!")

    # 8. Kiểm tra Dấu hiệu CAN THIỆP GAME (PMT3 / HACK / MOD)
    cheat_keywords = [
        'hack', 'cheat', 'modmenu', 'mod-menu', 'script', 'delta', 'fluxus', 'hydrogen', 
        'executors', 'aimbot', 'wallhack', 'modgame', 'hackgame', 'modapk', 'hackmap'
    ]
    found_cheat = [kw for kw in cheat_keywords if kw in url_lower]
    if found_cheat:
        score += 50
        reasons.append(f"🎮 **Dấu hiệu CAN THIỆP GAME (PMT3 / HACK / MOD):** Phát hiện từ khóa gian lận game (`{', '.join(found_cheat)}`). Sử dụng các file/script này nguy cơ cao bị **BAN/Khóa tài khoản vĩnh viễn** và bị cài Keylogger trộm nick!")

    # 9. Kiểm tra Dấu hiệu WEB CHỨA MÃ ĐỘC / VIRUS / ĐỘC HẠI
    malware_keywords = ['virus', 'trojan', 'keylogger', 'stealer', 'ransomware', 'miner', 'exploit', 'get-key', 'getkey']
    virus_exts = ['.exe', '.apk', '.bat', '.cmd', '.scr', '.vbs', '.iso', '.zip', '.rar']
    
    found_malware_kw = [kw for kw in malware_keywords if kw in url_lower]
    found_virus_ext = [ext for ext in virus_exts if path.endswith(ext) or url_lower.endswith(ext)]
    
    short_link_services = ['bit.ly', 'tinyurl.com', 'is.gd', 'cutt.ly', 'goo.gl', 't.co']
    is_short_link = any(s in domain for s in short_link_services)

    if found_malware_kw or found_virus_ext:
        score += 50
        kw_ext_list = found_malware_kw + found_virus_ext
        reasons.append(f"🦠 **CẢNH BÁO MÃ ĐỘC / VIRUS (MALWARE):** Dẫn trực tiếp tới file thực thi hoặc từ khóa mã độc (`{', '.join(kw_ext_list)}`). Nguy cơ bị đào tiền ảo ẩn, dính Ransomware tống tiền hoặc bị chiếm quyền thiết bị!")
    elif is_short_link:
        score += 20
        reasons.append("🔗 **Link rút gọn:** Web sử dụng dịch vụ ẩn đường dẫn thật để giấu link độc hại.")

    # 10. Kiểm tra Dấu hiệu SHOP FAKE & BÁN ACC (Tích hợp cảnh báo sau 1/7/2026)
    game_keywords = ['roblox', 'ff', 'freefire', 'lienquan', 'pubg', 'genshin', 'robux', 'bloxfruit']
    shop_keywords = ['shop', 'acc', 'nick', 'giare', 'random', 'banacc', 'muaacc', 'vongquay', 'kimcuong']
    celebrities = ['mixi', 'domixi', 'cris', 'crisdevil', 'pewpew', 'linhngocdam', 'thaydau', 'baconcon', 'tuyenmou']

    has_game_or_shop = any(kw in url_lower for kw in game_keywords + shop_keywords)
    found_celeb = [c for c in celebrities if c in url_lower]

    if has_game_or_shop:
        score += 50
        reasons.append("🚨 **CẢNH BÁO SHOP GAME GIẢ MẠO (QUY ĐỊNH 01/07/2026):** Phát hiện dịch vụ shop bán acc/vật phẩm game. Sau mốc 01/07/2026, hầu hết shop game đều đã bị cấm/khai tử. Web này gần như **100% LÀ GIẢ MẠO / LỪA ĐẢO NẠP TIỀN**!")

    # Thêm các bằng chứng an toàn tổng quát nếu không dính vi phạm
    if not found_cheat and not found_gambling and not found_adult and not found_malware_kw and not has_game_or_shop:
        safe_evidences.append("🛡️ **Nội dung sạch:** Không tìm thấy từ khóa cờ bạc, phim 18+, tool hack, shop game khai tử hay mã độc.")

    # Cảnh báo nguy hiểm tổng thể
    if score >= 50:
        reasons.append("🤣 **Cảnh báo: Link này nguy hiểm lắm, nhấn vào sẽ chặt tay! 🪓😜**")

    return score, reasons, safe_evidences

# Nút xử lý kiểm tra
if st.button("🔍 Kiểm Tra Ngay", use_container_width=True):
    if not url_input.strip():
        st.warning("⚠️ Vui lòng dán link cần kiểm tra!")
    else:
        risk_score, warnings, evidences = analyze_url(url_input)
        st.divider()
        
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
            st.write("📌 **Dẫn chứng an toàn phân tích được:**")
            for e in evidences:
                st.write(f"- {e}")

# Dòng Note ghi chú ở cuối trang
st.markdown("---")
st.caption("📌 *(NOTE: Đây ms là phiên bản Beta và cũng là dự án đầu tay của chúng mình nếu có sai sót mong mọi người thông cảm và bỏ qua , trong tương lai sẽ cs những bản Mega update.Xin cảm ơn)*")
