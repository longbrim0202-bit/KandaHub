import streamlit as st
import time

# Tiêu đề trang web
st.title("=== LOGIN ROBLOX ===")

# Tạo các ô nhập liệu trên Web
user = st.text_input("Nhập tài khoản:")
password = st.text_input("Nhập mật khẩu:", type="password")

# Nút bấm Đăng nhập
if st.button("Đăng nhập"):
    if user == "anrauma" and password == "longtop1":
        st.success(f"-> Login thành công em! Chào mừng {user}!")
        
        # Tạo vị trí hiển thị đồng hồ đếm ngược
        timer_placeholder = st.empty()
        
        # Vòng lặp đếm ngược từ 10 về 0 giây
        for seconds in range(10, -1, -1):
            timer_placeholder.info(f"⏳ Đang chờ vào game... còn {seconds} giây!")
            time.sleep(1)  # Tạm dừng 1 giây mỗi lần đếm
            
        st.balloons()  # Hiệu ứng pháo hoa khi đếm xong
        timer_placeholder.success("fuck ngu lm em hehe Đã đếm xong! Bắt đầu chơi thôi!")
        
    else:
        st.error("-> Login đần! Thì cút nha.")
