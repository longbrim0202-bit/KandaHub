import streamlit as st
import urllib.parse
import re

# Cấu hình giao diện trang web
st.set_page_config(page_title="Check Link Tự Động", page_icon="🛡️")

# =========================================================
# ⚙️ CẤU HÌNH GIAO DIỆN & PHÔNG NỀN
# =========================================================
# Link ảnh nền trực tiếp (đã chuẩn hóa định dạng i.ibb.co)
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

# --- NỘI DUNG WEB ---
st.title("🛡️ Check Link/URL(MADE BY MORI AND MIRUXZ")
st.write("Dán đường dẫn (URL) vào bên dưới để hệ thống quét và phân tích độ an toàn:")

url_input = st.text_input("", placeholder="Ví dụ: https://facebook.com hoặc http://vebo-tv.xyz", label_visibility="collapsed")

def analyze_url(url):
    """Hàm phân tích độ uy tín của URL"""
    score = 0
    reasons = []
    url_lower = url.lower()
    
    # 1. Kiểm tra HTTPS
    if not url_lower.startswith("https://"):
        score += 20
        reasons.append("⚠️ Web không có HTTPS (chỉ dùng HTTP, dễ bị chặn hoặc rò rỉ dữ liệu).")
        
    try:
        parsed = urllib.parse.urlparse(url if "://" in url else "http://" + url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        if not domain or "." not in domain:
            raise ValueError("Invalid domain")
    except:
        return 100, ["🚨 Định dạng đường dẫn bị lỗi! 😂 Nhấn vào sẽ chặt tay! 🪓🤣"]

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

    # 4. Kiểm tra Dấu hiệu CÁ ĐỘ / TÀI XỈU / ĐÁNH BẠC
    gambling_keywords = [
        'taixiu', 'tai-xiu', 'xocdia', 'xoc-dia', 'bet', 'casino', 'cacuoc', 'nhacai', 
        'keonhacai', 'kubet', 'shbet', '88bet', 'fun88', 'w88', 'f8bet', 'jun88', 
        'hi88', 'baccarat', 'slot', 'gamebai', 'nohu', 'danhbac', 'kèo', 'sunwin', 'go88'
    ]
    found_gambling = [kw for kw in gambling_keywords if kw in url_lower]
    if found_gambling:
        score += 45
        reasons.append(f"🎰 **Dấu hiệu TÀI XỈU / CÁ ĐỘ / CỜ BẠC:** Chứa từ khóa nhà cái, tài xỉu (`{', '.join(found_gambling)}`). Rất dễ bị ngấm mã độc và mất tiền!")

    # 5. Kiểm tra Dấu hiệu BÓNG ĐÁ LẬU / XEM CHÙA
    pirate_football_keywords = [
        'xoilac', 'vebo', 'mitom', 'socolive', 'cakhia', 'rautuoc', '90phut', 
        'tiengruoi', 'truoctiepbongda', 'tructiepbongda', 'livebongda', 'linkbongda'
    ]
    found_football = [kw for kw in pirate_football_keywords if kw in url_lower]
    if found_football:
        score += 35
        reasons.append(f"⚽ **Dấu hiệu BÓNG ĐÁ LẬU:** Nhận diện web xem bóng đá chui (`{', '.join(found_football)}`). Các web này thường gài dày đặc quảng cáo cờ bạc, mã độc tự nhảy pop-up!")

    # 6. Kiểm tra Dấu hiệu WEB PHIM 18+ / ĐỒI TRỤY
    adult_keywords = [
        'porn', 'hentai', 'sex', '18plus', 'phim18', 'jav', 'vlxx', 'xnx', 
        'phimsex', 'lon', 'cuclip', 'clipnong', 'loncon', 'thang18'
    ]
    found_adult = [kw for kw in adult_keywords if kw in url_lower]
    if found_adult:
        score += 45
        reasons.append(f"🔞 **Dấu hiệu WEB PHIM 18+ / NỘI DUNG ĐỒI TRỤY:** Chứa từ khóa nhạy cảm (`{', '.join(found_adult)}`). Các trang này chứa mật độ virus và lừa đảo đánh cắp thông tin cá nhân cực kỳ cao!")

    # 7. Kiểm tra Dấu hiệu SHOP FAKE & BÁN ACC
    game_keywords = ['roblox', 'ff', 'freefire', 'lienquan', 'pubg', 'genshin', 'robux', 'bloxfruit']
    shop_keywords = ['shop', 'acc', 'nick', 'giare', 'random', 'banacc', 'muaacc', 'vongquay', 'kimcuong']
    celebrities = ['mixi', 'domixi', 'cris', 'crisdevil', 'pewpew', 'linhngocdam', 'thaydau', 'baconcon', 'tuyenmou']

    has_game_or_shop = any(kw in url_lower for kw in game_keywords + shop_keywords)
    found_celeb = [c for c in celebrities if c in url_lower]

    if has_game_or_shop and found_celeb:
        score += 40
        reasons.append(f"🎭 **Dấu hiệu SHOP FAKE NGƯỜI NỔI TIẾNG:** Phát hiện tên Idol/Streamer (`{', '.join(found_celeb)}`) kết hợp với shop bán acc/robux. Hầu hết Streamer KHÔNG mở shop bán acc, coi chừng lừa đảo!")
    elif has_game_or_shop:
        score += 15
        reasons.append("🎮 Phát hiện dịch vụ Shop Game / Bán Acc / Vòng quay may mắn. Cần kiểm tra kỹ uy tín trước khi nạp tiền.")

    # 8. Kiểm tra Dấu hiệu NGUY CƠ VIRUS / FILE ĐỘC HẠI
    virus_exts = ['.exe', '.apk', '.bat', '.cmd', '.scr', '.vbs', '.iso', '.zip', '.rar']
    found_virus_ext = [ext for ext in virus_exts if path.endswith(ext) or url_lower.endswith(ext)]
    
    short_link_services = ['bit.ly', 'tinyurl.com', 'is.gd', 'cutt.ly', 'goo.gl', 't.co']
    is_short_link = any(s in domain for s in short_link_services)

    if found_virus_ext:
        score += 50
        reasons.append(f"🦠 **CẢNH BÁO VIRUS / ĐỘC HẠI:** Link dẫn thẳng tới file thực thi/nén (`{', '.join(found_virus_ext)}`). Nhấn vào có thể bị dính mã độc tống tiền hoặc bị chiếm quyền thiết bị!")
    elif is_short_link:
        score += 20
        reasons.append("🔗 **Link rút gọn:** Web sử dụng dịch vụ ẩn đường dẫn thật để giấu link độc hại.")

    # 9. Kiểm tra Giả mạo Thương hiệu lớn
    brands = ['facebook', 'google', 'paypal', 'shopee', 'momo', 'chinhphu', 'vtv', 'telegram', 'zalo']
    for brand in brands:
        if brand in domain and not (domain.endswith(f"{brand}.com") or domain.endswith(f"{brand}.vn")):
            score += 35
            reasons.append(f"🚨 Có dấu hiệu giả mạo thương hiệu lớn **{brand.upper()}**!")

    # Cảnh báo nguy hiểm tổng thể
    if score >= 50:
        reasons.append("🤣 **Cảnh báo: Link này nguy hiểm lắm, nhấn vào sẽ chặt tay! 🪓😜**")

    return score, reasons

# Nút xử lý kiểm tra
if st.button("🔍 Kiểm Tra Ngay", use_container_width=True):
    if not url_input.strip():
        st.warning("⚠️ Vui lòng dán link cần kiểm tra!")
    else:
        risk_score, warnings = analyze_url(url_input)
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
            st.write("Không phát hiện dấu hiệu lừa đảo phổ biến.")

# Dòng Note ghi chú ở cuối trang
st.markdown("---")
st.caption("📌 *(NOTE: Đây ms là phiên bản Beta xin mọi người thông cảm nếu có thông tin sai lệch trọng, trong tương lai sẽ cs những bản Mega update.Xin cảm ơn)*")
