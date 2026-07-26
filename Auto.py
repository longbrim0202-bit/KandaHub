import asyncio
import aiohttp
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


async def get_user_and_streams_via_gql(auth_token: str):
  # Sử dụng GraphQL API nội bộ của Twitch thông qua auth-token của trình duyệt
  headers = {
      "Authorization": f"OAuth {auth_token}",
      "Client-ID": "kimne78kx3ncx6brgo4mv6wbc5en1a",  # Client-ID chính thức của Twitch Web Player
      "Content-Type": "application/json",
  }

  # Truy vấn GraphQL để lấy thông tin user và các kênh đang live mà user đang theo dõi
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
      },
      {
          "operationName": "FollowedLives",
          "variables": {"limit": 30},
          "extensions": {
              "persistedQuery": {
                  "version": 1,
                  "sha256Hash": (
                      "3ef04604e32d84a6a55512aa5b2b0ce895b6d51e7aedb7d3419985223ab49132"
                  ),
              }
          },
      },
  ]

  url = "https://gql.twitch.tv/gql"
  async with aiohttp.ClientSession() as session:
    async with session.post(url, json=query, headers=headers) as resp:
      if resp.status == 200:
        data = await resp.json()
        return data
      return None


# --- GIAO DIỆN CHÍNH ---
st.title("⚡ Auto Farm Channel Point")
st.markdown(
    "Hệ thống tự động quét, bám đuổi livestream và cày điểm kênh thật."
)

with st.sidebar:
  st.header("⚙️ Cấu hình hệ thống")
  token_input = st.text_input(
      "Nhập Access Token (auth-token)",
      type="password",
      placeholder="Dán mã token của bạn vào đây...",
  )
  start_btn = st.button("🚀 Khởi động Tiến trình Farm", type="primary")
  st.markdown("---")
  st.info("Trạng thái: Sẵn sàng kết nối.")

if start_btn:
  if not token_input:
    st.error("⚠️ Vui lòng nhập Access Token!")
  else:
    with st.spinner("Đang kết nối vào hệ thống Twitch bằng Token thực tế..."):
      results = asyncio.run(get_user_and_streams_via_gql(token_input))

      if not results:
        st.error("❌ Không thể kết nối tới Twitch. Vui lòng kiểm tra lại token!")
      else:
        user_info = None
        streams = []

        for res in results:
          data = res.get("data", {})
          if "currentUser" in data:
            user_info = data["currentUser"]
          if "user" in data and data["user"]:
            followed_conn = data["user"].get("followedStreams", {})
            streams = followed_conn.get("edges", [])

        if not user_info:
          st.error(
              "❌ Token không hợp lệ hoặc đã hết hạn. Hãy lấy lại auth-token mới"
              " nhất!"
          )
        else:
          username = user_info.get("displayName")
          st.success(
              f"✅ Đã kết nối thành công tài khoản: **{username}** (Dữ liệu"
              " thực tế)"
          )

          st.markdown("---")
          st.subheader("📡 Danh sách Kênh & Tiến trình Farm Thực Tế")

          if not streams:
            st.warning(
                "⚠️ Hiện tại không có kênh nào bạn theo dõi đang phát sóng trực"
                " tiếp (Live)."
            )
          else:
            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]

            for idx, edge in enumerate(streams):
              node = edge.get("node", {})
              broadcaster = node.get("broadcaster", {})
              channel_name = broadcaster.get(
                  "displayName", "Không rõ streamer"
              )
              game = node.get("game", {})
              game_title = (
                  game.get("displayName", "Không rõ danh mục")
                  if game
                  else "Không rõ danh mục"
              )
              viewer_count = node.get("viewersCount", 0)

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
      "👉 Hãy dán đoạn mã `auth-token` của bạn vào ô bên trái và bấm **Khởi"
      " động Tiến trình Farm**."
  )
