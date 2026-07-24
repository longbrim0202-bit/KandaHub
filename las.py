import streamlit as st
import urllib.parse
import re

# Cấu hình giao diện trang web
st.set_page_config(page_title="Check Link Tự Động", page_icon="🛡️")

st.title("🛡️ Check Verity Link/URL ( MADE By Miruxz")
st.write("Dán đường dẫn (URL) vào bên dưới để hệ thống quét và phân tích độ an toàn:")

# Ô nhập link
url_input = st.text_input("", placeholder="Ví dụ: https://facebook.com hoặc http://paypal-security.xyz", label_visibility="collapsed")

def analyze_url(url):
    """Hàm phân tích độ uy tín của URL"""
    score = 0
    reasons = []
    
    # 1. Kiểm tra HTTPS
    if not url.startswith("https://"):
        score += 20
        reasons.append("⚠️ Web không có HTTPS (chỉ dùng HTTP).")
        
    try:
        parsed = urllib.parse.urlparse(url if "://" in url else "http://" + url)
        domain = parsed.netloc.lower()
    except:
        return 100, ["🚨 Định dạng đường dẫn bị lỗi!"]

    # 2. Kiểm tra nếu dùng IP thay cho tên miền
    ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    if re.match(ip_pattern, domain):
        score += 40
        reasons.append("🚨 Sử dụng địa chỉ IP trực tiếp (Rủi ro lừa đảo rất cao!).")

    # 3. Kiểm tra đuôi tên miền rủi ro
    risky_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.zip', '.top', '.work', '.xyz', '.cc']
    if any(domain.endswith(tld) for tld in risky_tlds):
        score += 25
        reasons.append("⚠️ Sử dụng đuôi tên miền miễn phí/rủi ro (.xyz, .tk, .zip...).")

    # 4. Kiểm tra từ khóa nhạy cảm
    keywords = ['login', 'verify', 'account', 'secure', 'banking', 'update', 'free', 'gift', 'napthe', 'nhankimcuong']
    found_words = [kw for kw in keywords if kw in url.lower()]
    if found_words:
        score += 20
        reasons.append(f"⚠️ Chứa từ khóa nhạy cảm: `{', '.join(found_words)}`")

    # 5. Kiểm tra giả mạo thương hiệu
    brands = ['facebook', 'google', 'paypal', 'shopee', 'momo', 'chinhphu', 'vtv']
    for brand in brands:
        if brand in domain and not (domain.endswith(f"{brand}.com") or domain.endswith(f"{brand}.vn")):
            score += 35
            reasons.append(f"🚨 Có dấu hiệu giả mạo thương hiệu **{brand.upper()}**!")

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
