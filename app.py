import streamlit as st
import time

# --- 1. CẤU HÌNH PHÔNG NỀN (CSS) ---
# Dán link ảnh của bạn vào ô bên dưới:
MY_BACKGROUND_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDR-P5KHGQ319u8LAXSPsvdlJ6YW6yfDNwTZXCbGKb2w&s=10"

st.markdown(f"""
    <style>
    /* Chỉnh phông nền cho toàn bộ trang web */
    [data-testid="stAppViewContainer"] {{
        background-image: url("{MY_BACKGROUND_IMAGE_URL}");
        background-size: cover; /* Phủ kín màn hình */
        background-position: center; /* Căn giữa */
        background-repeat: no-repeat; /* Không lặp lại */
        background-attachment: fixed; /* Giữ nguyên khi cuộn chuột */
    }}

    /* Chỉnh cho phần nội dung chính không bị che khuất */
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0); /* Trong suốt header */
    }}
    
    /* Chỉnh font chữ Montserrat từ Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'Montserrat', sans-serif;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. NỘI DUNG WEB LOGIN ---
st.title("=== LOGIN ROBLOX ===")

user = st.text_input("Nhập tài khoản:")
password = st.text_input("Nhập mật khẩu:", type="password")

if st.button("Đăng nhập"):
    if user == "anrauma" and password == "longtop1":
        st.success(f"-> Login thành công em! Chào mừng {user}!")
        
        timer_placeholder = st.empty()
        for seconds in range(10, -1, -1):
            timer_placeholder.info(f"⏳ Đang chờ vào game... còn {seconds} giây!")
            time.sleep(1)
            
        st.balloons()
        timer_placeholder.success("🚀 Đã đếm xong! Bắt đầu chơi thôi!")
    else:
        st.error("-> Login đần! Thì cút nha.")
