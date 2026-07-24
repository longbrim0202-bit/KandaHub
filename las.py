import streamlit as st
import urllib.parse
import re

# Cấu hình giao diện trang web
st.set_page_config(page_title="Check URL/LINK(BY MIRUXZ AND MORI)", page_icon="🛡️")

# --- Ô NHẬP LINK ẢNH NỀN TÙY CHỌN ---
st.subheader("🖼️ Tùy Chỉnh Phông Nền")
bg_image_url = st.text_input(
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRd-owPNbKUVBeZOssR_5MQ3u_ci4PLrW3czNa0wn8_NQ&s=10:",
    value="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1920&auto=format&fit=crop", # Link ảnh mặc định
    placeholder="https://example.com/anh-nen.jpg"
)

# Áp dụng CSS để đổi nền theo URL nhập vào
if bg_image_url.strip():
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{bg_image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.90); /* Lớp phủ sáng giúp rõ chữ */
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            margin-top: 1rem;
        }}
        </style>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- PHẦN QUÉT LINK AN TOÀN ---
st.title("🛡️ Kiểm Tra Độ Uy Tín Của Link")
st.write("Dán đường dẫn (URL) cần kiểm tra vào bên dưới để hệ thống quét và phân tích:")

# Ô nhập link cần check
url_input = st.text_input("", placeholder="Ví dụ: https://facebook.com hoặc http://shopmixigaming-acc.xyz", label_visibility="collapsed")

def analyze_url(url):
    """Hàm phân tích độ uy tín của URL"""
    score = 0
    reasons = []
    url_lower = url.lower()
    
    # 1. Kiểm tra HTTPS
    if not url_lower.startswith("https://"):
        score += 20
        reasons.append("⚠️ Web không có HTTPS (chỉ dùng HTTP).")
        
    try:
        parsed = urllib.parse.urlparse(url if "://" in url else "http://" + url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        if not domain or "." not in domain:
            raise ValueError("Invalid domain")
    except:
        return 100, ["🚨 Định dạng đường dẫn bị lỗi! 😂 Nhấn vào sẽ chặt tay! 🪓🤣"]

    # 2. Kiểm tra nếu dùng IP thay cho tên miền
    ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    if re.match(ip_pattern, domain):
        score += 40
        reasons.append("🚨 Sử dụng địa chỉ IP trực tiếp (Rủi ro lừa đảo rất cao!).")

    # 3. Kiểm tra đuôi tên miền rủi ro
    risky_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.zip', '.top', '.work', '.xyz', '.cc', '.club', '.vip', '.site', '.online']
    if any(domain.endswith(tld) for tld in risky_tlds):
        score += 25
        reasons.append("⚠️ Sử dụng đuôi tên miền rẻ/miễn phí có rủi ro cao (.xyz, .tk, .vip, .club...).")

    # 4. Kiểm tra Dấu hiệu CÁ ĐỘ / ĐÁNH BẠC
    gambling_keywords = [
        'bet', 'casino', 'cacuoc', 'nhacai', 'keonhacai', 'kubet', 'shbet', 
        '88bet', 'fun88', 'w88', 'f8bet', 'jun88', 'hi88', 'baccarat', 
        'taixiu', 'xocdia', 'slot', 'gamebai', 'nohu', 'danhbac', 'kèo'
    ]
    found_gambling = [kw for kw in gambling_keywords if kw in url_lower]
    if found_gambling:
        score += 45
        reasons.append(f"🎰 **Dấu hiệu CÁ ĐỘ / ĐÁNH BẠC:** Chứa từ khóa nhà cái/cá cược (`{', '.join(found_gambling)}`). Hãy cẩn thận rủi ro vi phạm pháp luật và mất tiền!")

    # 5. Kiểm tra Dấu hiệu SHOP FAKE & BÁN ACC
    game_keywords = ['roblox', 'ff', 'freefire', 'lienquan', 'pubg', 'genshin', 'robux', 'bloxfruit']
    shop_keywords = ['shop', 'acc', 'nick', 'giare', 'random', 'banacc', 'muaacc', 'vongquay', 'kimcuong']
    celebrities = ['mixi', 'domixi', 'cris', 'crisdevil', 'pewpew', 'linhngocdam', 'thaydau', 'baconcon', 'tuyenmou']

    has_game_or_shop = any(kw in url_lower for kw in game_keywords + shop_keywords)
    found_celeb = [c for c in celebrities if c in url_lower]

    if has_game_or_shop and found_celeb:
        score += 40
        reasons.append(f"🎭 **Dấu hiệu SHOP FAKE NGƯỜI NỔI TIẾNG:** Phát hiện tên Streamer/Idol (`{', '.join(found_celeb)}`) kết hợp với shop bán acc/robux. Rất nhiều Idol KHÔNG mở shop bán acc, coi chừng bị lừa tiền!")
    elif has_game_or_shop:
        score += 15
        reasons.append("🎮 Phát hiện dịch vụ Shop Game / Bán Acc / Vòng quay may mắn. Cần kiểm tra kỹ uy tín trước khi nạp tiền.")

    # 6. Kiểm tra Dấu hiệu NGUY CƠ DĨNH VIRUS / ĐỘC HẠI (MALWARE)
    virus_exts = ['.exe', '.apk', '.bat', '.cmd', '.scr', '.vbs', '.iso', '.zip', '.rar']
    found_virus_ext = [ext for ext in virus_exts if path.endswith(ext) or url_lower.endswith(ext)]
    
    short_link_services = ['bit.ly', 'tinyurl.com', 'is.gd', 'cutt.ly', 'goo.gl', 't.co']
    is_short_link = any(s in domain for s in short_link_services)

    if found_virus_ext:
        score += 50
        reasons.append(f"🦠 **CẢNH BÁO VIRUS / ĐỘC HẠI:** Link dẫn thẳng tới file thực thi/nén (`{', '.join(found_virus_ext)}`). Nhấn vào có thể bị tải virus, mã độc tống tiền hoặc chiếm quyền máy tính/điện thoại!")
    elif is_short_link:
        score += 20
        reasons.append("🔗 **Link rút gọn:** Web sử dụng dịch vụ ẩn đường dẫn thật, hãy cẩn thận kẻ gian giấu link cài virus hoặc mã độc bên trong.")
    elif len(url) > 100:
        score += 15
        reasons.append("🧬 **Link quá dài / bất thường:** Độ dài URL bất thường, thường dùng để chèn mã độc hoặc che giấu hành vi lừa đảo.")

    # 7. Kiểm tra giả mạo thương hiệu lớn
    brands = ['facebook', 'google', 'paypal', 'shopee', 'momo', 'chinhphu', 'vtv', 'telegram', 'zalo']
    for brand in brands:
        if brand in domain and not (domain.endswith(f"{brand}.com") or domain.endswith(f"{brand}.vn")):
            score += 35
            reasons.append(f"🚨 Có dấu hiệu giả mạo thương hiệu lớn **{brand.upper()}**!")

    # Cảnh báo nguy hiểm chung
    if score >= 50:
        reasons.append("🤣 **Cảnh báo: Link này nguy hiểm lắm, nhấn vào sẽ chặt tay! 🪓😜**")

    return score, reasons

# Nút kiểm tra
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
