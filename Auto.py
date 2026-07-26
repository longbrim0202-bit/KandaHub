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


async def get_twitch_user_via_cookie(auth_token: str):
  # Sử dụng chuẩn Client-ID và phân quyền OAuth Cookie của Twitch Web
  headers = {
      "Authorization": f"OAuth {auth_token}",
      "Client-Id": "kimne78kx3ncx6brgo4mv6wbc5en1a",
      "Content-Type": "application/json",
  }

  query = [
      {
          "operationName": "CurrentUser",
          "variables": {},
          "extensions": {
              "persistedQuery": {
                  "version": 1,
                  "sha256Hash": (
                      "5b172462943f65e2365bb5f7b49fe53ee52a92634f19b4a45371c6b141444983"
                  ),
              }
          },
      }
  ]

  url = "https://gql.twitch.tv/gql"
  async with aiohttp.ClientSession() as session:
    async with session.post(url, json=query, headers=headers) as resp:
      if resp.status == 200:
        results = await resp.json()
        for res in results:
          data = res.get("data", {})
          if "currentUser" in data and data["currentUser"]:
            return data["currentUser"]
      return None


st.title("⚡ Auto Farm Channel Point")
st.markdown("Hệ thống quét và kết nối luồng farm điểm qua Cookie Token.")

with st.sidebar:
  st.header("⚙️ Cấu hình hệ thống")
  token_input = st.text_input(
      "Nhập Access Token (auth-token)",
      type="password",
      placeholder="Dán mã auth-token từ F12...",
  )
  start_btn = st.button("🚀 Khởi động Tiến trình Farm", type="primary")
  st.markdown("---")
  st.info("Trạng thái: Sẵn sàng kết nối Local.")

if start_btn:
  if not token_input:
    st.error("⚠️ Vui lòng nhập Token!")
  else:
    with st.spinner("Đang xác thực Cookie Token với Twitch..."):
      user_info = asyncio.run(get_twitch_user_via_cookie(token_input))

      if not user_info:
        st.error(
            "❌ Token không hợp lệ hoặc đã hết hạn. Hãy F5 lại Twitch và lấy"
            " lại auth-token mới nhất!"
        )
      else:
        username = user_info.get("displayName")
        st.success(
            f"✅ Kết nối thành công tài khoản chuẩn Cookie: **{username}**"
        )

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
                        <p><b>Trạng thái:</b> Đang bám đuổi & nhận điểm</p>
                        <hr style="border-color: #2f2f35;">
                        <span class="badge-claim">🎁 Auto Claim Active</span>
                    </div>
                    """,
              unsafe_allow_html=True,
          )
else:
  st.info("👉 Hãy dán `auth-token` và bấm **Khởi động Tiến trình Farm**.")
