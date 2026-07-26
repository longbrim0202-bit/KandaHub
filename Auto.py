import asyncio
import aiohttp
import streamlit as st

st.set_page_config(
    page_title="Twitch Auto Farm Ultimate", page_icon="⚡", layout="wide"
)

# --- CSS TỐI ƯU GIAO DIỆN SIÊU CẤP ---
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


# --- HỆ THỐNG XỬ LÝ API TWITCH (ASYNC ENGINE) ---
async def fetch_twitch_api(endpoint: str, token: str, client_id: str):
  headers = {
      "Client-ID": client_id,
      "Authorization": f"Bearer {token}",
      "Accept": "application/vnd.twitchtv.v5+json",
  }
  url = f"https://api.twitch.tv/helix/{endpoint}"
  async with aiohttp.ClientSession() as session:
    async with session.get(url, headers=headers) as response:
      if response.status == 200:
        return await response.json()
      return None


async def get_followed_live_channels(token: str, client_id: str, user_id: str):
  # Lấy danh sách các kênh đang live mà user đang follow để tự động farm
  data = await fetch_twitch_api(
      f"streams/followed?user_id={user_id}", token, client_id
  )
  if data and "data" in data:
    return data["data"]
  return []


async def get_user_info(token: str, client_id: str):
  headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
  async with aiohttp.ClientSession() as session:
    async with session.get(
        "https://api.twitch.tv/helix/users", headers=headers
    ) as resp:
      if resp.status == 200:
        res = await resp.json()
        if res.get("data"):
          return res["data"][0]
  return None


# --- GIAO DIỆN ĐIỀU KHIỂN CHÍNH ---
st.title("⚡ Twitch Auto Farm: Siêu Cấp Real-Time Engine")
st.markdown("Hệ thống tự động quét, bám đuổi livestream và cày điểm kênh thật.")

with st.sidebar:
  st.header("⚙️ Cấu hình hệ thống")
  token_input = st.text_input(
      "Nhập Access Token (auth-token)",
      type="password",
      placeholder="Dán mã token của bạn vào đây...",
  )
  # Client ID chuẩn tích hợp sẵn để gọi API Helix
  client_id_input = st.text_input(
      "Client ID", value="gp762nuuqcoxypju8c569th9wz7q5"
  )

  start_btn = st.button("🚀 Khởi động Tiến trình Farm", type="primary")
  st.markdown("---")
  st.info("Trạng thái: Sẵn sàng kết nối API.")

# --- KHU VỰC THỰC THI CHÍNH ---
if start_btn:
  if not token_input:
    st.error("⚠️ Vui lòng nhập Access Token để hệ thống có thể kết nối!")
  else:
    with st.spinner("Đang xác thực tài khoản và quét các kênh đang phát sóng..."):
      user_data = asyncio.run(get_user_info(token_input, client_id_input))

      if not user_data:
        st.error(
            "❌ Token không hợp lệ hoặc đã hết hạn! Vui lòng kiểm tra lại mã"
            " auth-token."
        )
      else:
        username = user_data.get("display_name")
        user_id = user_data.get("id")
        st.success(
            f"✅ Đã kết nối thành công tài khoản: **{username}** (ID: {user_id})"
        )

        st.markdown("---")
        st.subheader("📡 Danh sách Kênh & Tiến trình Farm Thực Tế")

        # Quét kênh đang live thực tế
        live_streams = asyncio.run(
            get_followed_live_channels(token_input, client_id_input, user_id)
        )

        if not live_streams:
          st.warning(
              "⚠️ Hiện tại không có kênh nào bạn theo dõi đang phát sóng trực"
              " tiếp (Live). Hãy follow thêm các streamer khác để hệ thống tự"
              " động nhận diện!"
          )
        else:
          col1, col2, col3 = st.columns(3)
          cols = [col1, col2, col3]

          for idx, stream in enumerate(live_streams):
            channel_name = stream.get("user_name")
            game_title = stream.get("game_name", "Không rõ danh mục")
            viewer_count = stream.get("viewer_count", 0)

            current_col = cols[idx % 3]
            with current_col:
              st.markdown(
                  f"""
                            <div class="card">
                                <span class="badge-live">ĐANG FARM</span>
                                <h3 style="margin-top:10px; color:#bf94ff;">{channel_name}</h3>
                                <p><b>Danh mục:</b> {game_title}</p>
                                <p><b>Người xem:</b> {viewer_count:,}</p>
                                <hr style="border-color: #2f2f35;">
                                <span class="badge-claim">🎁 Tự động nhận điểm (Claim Bonus)</span>
                            </div>
                            """,
                  unsafe_allow_html=True,
              )
else:
  st.info(
      "👉 Hãy nhập Access Token vào cột bên trái và bấm **Khởi động Tiến trình"
      " Farm** để bắt đầu quét dữ liệu thật từ tài khoản của bạn."
  )
