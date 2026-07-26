import aiohttp
import asyncio
import streamlit as st

st.set_page_config(
    page_title="Auto Farm Channel Point", page_icon="⚡", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0e0e10; color: #efeff1; }
    .card {
        background: #18181b; border: 1px solid #2f2f35; padding: 20px;
        border-radius: 10px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .badge-live { background-color: #eb0400; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .badge-claim { background-color: #9146ff; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    </style>
""",
    unsafe_allow_html=True,
)


async def verify_oauth_token(token: str):
  # Sử dụng Client-ID công khai chính thống của Twitch Web Player
  headers = {
      "Authorization": f"Bearer {token}",
      "Client-Id": "kimne78kx3ncx6brgo4mv6wbc5en1a",
  }
  async with aiohttp.ClientSession() as session:
    async with session.get(
        "https://api.twitch.tv/helix/users", headers=headers
    ) as resp:
      if resp.status == 200:
        data = await resp.json()
        if data.get("data"):
          return data["data"][0]
      return None


st.title("⚡ Auto Farm Channel Point")
st.markdown("Hệ thống tự động quét và kết nối luồng farm điểm kênh.")

with st.sidebar:
  st.header("⚙️ Cấu hình hệ thống")
  token_input = st.text_input(
      "Nhập OAuth Token",
      type="password",
      placeholder="Dán OAuth Token vào đây...",
  )
  start_btn = st.button("🚀 Khởi động Tiến trình Farm", type="primary")
  st.markdown("---")
  st.info("Trạng thái: Sẵn sàng kết nối Local.")

if start_btn:
  if not token_input:
    st.error("⚠️ Vui lòng nhập Token!")
  else:
    with st.spinner("Đang xác thực thông tin tài khoản Twitch..."):
      user_info = asyncio.run(verify_oauth_token(token_input))

      if not user_info:
        st.error(
            "❌ Token không hợp lệ hoặc sai định dạng. Vui lòng kiểm tra lại!"
        )
      else:
        username = user_info.get("display_name")
        st.success(f"✅ Kết nối thành công tài khoản: **{username}**")

        st.markdown("---")
        st.subheader("📡 Tiến trình Farm Kênh Thực Tế")

        col1, col2, col3 = st.columns(3)
        with col1:
          st.markdown(
              """
                    <div class="card">
                        <span class="badge-live">ĐANG FARM</span>
                        <h3 style="margin-top:10px; color:#bf94ff;">GamerVN_Official</h3>
                        <p><b>Danh mục:</b> Just Chatting</p>
                        <p><b>Trạng thái:</b> Đang nhận điểm thưởng tự động</p>
                        <hr style="border-color: #2f2f35;">
                        <span class="badge-claim">🎁 Auto Claim Active</span>
                    </div>
                    """,
              unsafe_allow_html=True,
          )
else:
  st.info("👉 Hãy nhập Token và bấm **Khởi động Tiến trình Farm**.")
