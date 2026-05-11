import streamlit as st
from openai import OpenAI

# --------------------
# 기본 스타일 (CSS)
# --------------------
st.markdown("""
<style>
.chat-card {
    background-color: #1f1f1f;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 12px;
}
.tag {
    display: inline-block;
    background-color: #333;
    color: #fff;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    margin-right: 6px;
}
.title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 4px;
}
.reason {
    font-size: 14px;
    color: #ccc;
}
</style>
""", unsafe_allow_html=True)

# --------------------
# 제목 영역
# --------------------
st.title("🎮 게임 추천 AI")
st.caption("취향을 선택하면 어울리는 게임을 추천해 드려요")

# --------------------
# API Key
# --------------------
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("API 키를 입력하면 추천을 시작할 수 있어요 🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# --------------------
# 취향 선택 UI
# --------------------
st.subheader("🎯 당신의 취향을 알려주세요")

col1, col2, col3 = st.columns(3)

with col1:
    genre = st.selectbox(
        "장르",
        ["상관없음", "RPG", "액션", "어드벤처", "시뮬레이션", "인디"]
    )

with col2:
    platform = st.selectbox(
        "플랫폼",
        ["PC", "콘솔", "모바일"]
    )

with col3:
    play_style = st.selectbox(
        "플레이 방식",
        ["싱글 플레이", "멀티 플레이", "협동 플레이"]
    )

difficulty = st.radio(
    "난이도 선호",
    ["쉬움", "보통", "어려움"],
    horizontal=True
)

# --------------------
# 추천 버튼
# --------------------
if st.button("✨ 게임 추천받기"):
    prompt = f"""
    장르: {genre}
    플랫폼: {platform}
    플레이 방식: {play_style}
    난이도: {difficulty}

    위 조건에 맞는 게임을 3개 추천해줘.
    각 게임마다 추천 이유를 1~2문장으로 설명해줘.
    """

    with st.spinner("취향 분석 중... 🎮"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "너는 게임 추천 전문가다. 간결하고 이해하기 쉽게 추천한다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    result = response.choices[0].message.content

    # --------------------
    # 결과 출력 (카드 UI)
    # --------------------
    st.subheader("🕹️ 추천 결과")

    for block in result.split("\n\n"):
        if block.strip():
            st.markdown(
                f"""
                <div class="chat-card">
                    <div class="title">{block.splitlines()[0]}</div>
                    <div class="reason">{' '.join(block.splitlines()[1:])}</div>
                    <div style="margin-top:8px;">
                        <span class="tag">{genre}</span>
                        <span class="tag">{platform}</span>
                        <span class="tag">{play_style}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
