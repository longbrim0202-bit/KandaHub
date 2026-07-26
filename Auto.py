import streamlit as st

# Cấu hình giao diện trang web
st.set_page_config(page_title="Twitch Farm Dashboard", page_icon="🟣", layout="centered")

# =========================================================
# ⚙️ CẤU HÌNH GIAO DIỆN & CSS (DARK MODE)
# =========================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, div, button, input {
        font-family: 'Roboto', sans-serif !important;
    }
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main .block-container {
        background-color: #161920;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        margin-top: 1rem;
        border: 1px solid #262933;
    }
    .channel-card {
        background-color: #1a1c23;
        border: 1px solid #2d3139;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 🔐 QUẢN LÝ TRẠNG THÁI ĐĂNG NHẬP BẰNG TOKEN
# =========================================================
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "twitch_token" not in st.session_state:
    st.session_state.twitch_token = ""

# =========================================================
# 🎨 GIAO DIỆN SIDEBAR (HIỂN THỊ KHI ĐÃ ĐĂNG NHẬP)
# =========================================================
with st.sidebar:
    if st.session_state.is_logged_in:
        st.image("https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=100&h=100&fit=crop", width=60)
        st.markdown("### Tài khoản Twitch")
        st.caption("🟢 Đang chạy ngầm farm điểm")
        st.divider()
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.is_logged_in = False
            st.session_state.twitch_token = ""
            st.rerun()
    else:
        st.info("🔒 Vui lòng nhập Token Twitch ở màn hình chính để kết nối.")

# =========================================================
# 🎨 GIAO DIỆN CHÍNH
# =========================================================
st.title("🟣 Twitch Channel Points Auto Farm")
st.caption("Hệ thống tự động hóa cày điểm kênh Twitch bằng Token")
st.markdown("---")

# Kiểm tra trạng thái: Nếu chưa đăng nhập thì hiện form nhập Token
if not st.session_state.is_logged_in:
    st.write("### 🔑 Đăng Nhập Bằng Twitch Access Token")
    st.info("💡 Nhập chuỗi Token OAuth của bạn để hệ thống xác thực và mở giao diện farm điểm.")
    
    with st.form("twitch_token_form"):
        token_input = st.text_input("Nhập Twitch Access Token:", type="password")
        submit_login = st.form_submit_button("🚀 Xác Thực Token & Mở Dashboard", use_container_width=True)
        
        if submit_login:
            if token_input.strip():
                st.session_state.is_logged_in = True
                st.session_state.twitch_token = token_input.strip()
                st.success("🎉 Xác thực Token thành công! Đang chuyển vào Dashboard...")
                st.rerun()
            else:
                st.warning("Vui lòng nhập chuỗi Token hợp lệ!")

# Nếu đã đăng nhập thành công thì hiện Dashboard farm điểm
else:
    col_title, col_coin = st.columns([4, 1])
    with col_title:
        st.markdown("### 📊 Dashboard Quản Lý Farm Twitch")
    with col_coin:
        st.markdown("### 🟣 **8,500 Pts**")

    # Thanh thống kê tổng quan
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="📺 Kênh theo dõi", value="51")
    with m2:
        st.metric(label="✅ Đang cày", value="26")
    with m3:
        st.metric(label="🎁 Chờ nhận thưởng", value="1")
    with m4:
        st.metric(label="🟣 Điểm chờ nhận", value="200")

    st.markdown("---")
    st.markdown("### 📋 Danh sách Kênh & Tiến trình Farm")

    # Các thẻ thông tin kênh đang farm
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="channel-card">
                <span style="background-color: #d97706; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">🟢 Đang chạy</span>
                <h4 style="margin-top: 10px; color: white;">Kênh: GamerVN_Official</h4>
                <p style="color: gray; font-size: 14px;">Đang xem livestream Valorant</p>
                <hr style="border-color: #2d3139;">
                <p style="color: #c084fc; font-weight: bold;">🎁 +700 Points</p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
            <div class="channel-card">
                <span style="background-color: #2563eb; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">🟡 Chờ nhận thưởng</span>
                <h4 style="margin-top: 10px; color: white;">Kênh: ChillLofi_Stream</h4>
                <p style="color: gray; font-size: 14px;">Đang phát nhạc Lofi</p>
                <hr style="border-color: #2d3139;">
                <p style="color: #c084fc; font-weight: bold;">🎁 +200 Points</p>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
            <div class="channel-card">
                <span style="background-color: #16a34a; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">✅ Đã nhận</span>
                <h4 style="margin-top: 10px; color: white;">Kênh: TechReview_VN</h4>
                <p style="color: gray; font-size: 14px;">Đã hoàn thành phiên live</p>
                <hr style="border-color: #2d3139;">
                <p style="color: #c084fc; font-weight: bold;">🎁 +200 Points</p>
            </div>
        """, unsafe_allow_html=True)
