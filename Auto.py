import streamlit as st

# Thiết lập giao diện rộng
st.set_page_config(page_title="Twitch Farm Dashboard", page_icon="🎮", layout="wide")

# =========================================================
# 🎨 TÙY CHỈNH CSS CHO GIỐNG PHONG CÁCH GAMING / DARK MODE
# =========================================================
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Card thống kê */
    .metric-card {
        background-color: #1a1c23;
        border: 1px solid #2d3139;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
    }
    
    /* Card danh sách kênh */
    .channel-card {
        background-color: #161920;
        border: 1px solid #262933;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 📌 SIDEBAR ĐIỀU HƯỚNG
# =========================================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=100&h=100&fit=crop", width=60)
    st.markdown("### Kaineki")
    st.caption("🟢 Đang chạy ngầm")
    st.divider()
    
    st.page_link("app.label", label="📊 Dashboard", icon="🏠")
    st.page_link("app.label", label="⚙️ Cài đặt tài khoản", icon="⚙️")
    st.divider()
    st.info("💡 Trạng thái: Tool đang tự động kết nối API Twitch.")

# =========================================================
# 🖥️ GIAO DIỆN CHÍNH (DASHBOARD)
# =========================================================
col_title, col_coin = st.columns([4, 1])
with col_title:
    st.title("Dashboard Quản Lý Farm Twitch")
with col_coin:
    st.markdown("### 🟣 **8,500 Points**")

st.markdown("---")

# 1. Hàng thống kê tổng quan (Metrics)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="📺 Kênh theo dõi", value="51")
with m2:
    st.metric(label="✅ Đang cày", value="26")
with m3:
    st.metric(label="🎁 Chờ nhận thưởng", value="1")
with m4:
    st.metric(label="🟣 Điểm chờ nhận", value="200")

st.markdown("### 📋 Danh sách Kênh & Tiến trình Farm (32)")

# 2. Khu vực hiển thị các thẻ kênh (Cards Grid)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
        <div class="channel-card">
            <span style="background-color: #d97706; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">🟢 Đang chạy</span>
            <h4 style="margin-top: 10px;">Kênh: GamerVN_Official</h4>
            <p style="color: gray; font-size: 14px;">Đang xem livestream Valorant</p>
            <hr style="border-color: #262933;">
            <p style="color: #c084fc; font-weight: bold;">🎁 +700 Points</p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="channel-card">
            <span style="background-color: #2563eb; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">🟡 Chờ nhận thưởng</span>
            <h4 style="margin-top: 10px;">Kênh: ChillLofi_Stream</h4>
            <p style="color: gray; font-size: 14px;">Đang phát nhạc Lofi</p>
            <hr style="border-color: #262933;">
            <p style="color: #c084fc; font-weight: bold;">🎁 +200 Points</p>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
        <div class="channel-card">
            <span style="background-color: #16a34a; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">✅ Đã nhận</span>
            <h4 style="margin-top: 10px;">Kênh: TechReview_VN</h4>
            <p style="color: gray; font-size: 14px;">Đã hoàn thành phiên live</p>
            <hr style="border-color: #262933;">
            <p style="color: #c084fc; font-weight: bold;">🎁 +200 Points</p>
        </div>
    """, unsafe_allow_html=True)
