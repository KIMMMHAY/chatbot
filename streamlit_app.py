import streamlit as st
from openai import OpenAI

# --------------------
# CSS 스타일
# --------------------
st.markdown("""
<style>
.chat-bubble {
    padding: 14px 18px;
    border-radius: 18px;
    margin-bottom: 10px;
    max-width: 80%;
    line-height: 1.6;
}
.user {
    background-color: #2563eb;
    color: white;
    margin-left: auto;
}
.assistant {
    background-color: #1f2933;
    color: #e5e7eb;
}
.game-card {
    background-color: #111827;
    padding: 16px;
    border-radius: 14px;
    margin-top: 12px;
}
.game-title {
    font-size: 18px;
    font-weight: bold;
}
.game-desc {
    font-size: 14px;
    color: #d1d5db;
}
.tag {
    display: inline-block;
    font-size: 12px;
    background-color: #374151;
    padding: 4px 10px;
    border-radius: 999px;
    margin-right: 6px;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# --------------------
# 제목
# --------------------
st.title("🎮 게임 추천 AI 챗봇")
st.caption("대화로 취향을 파악해 게임을 추천해 드려요")

# --------------------
# API Key
# --------------------
openai_api_key = st.text_input("OpenAI API 키", type="password")
if not openai_api_key:
    st.info("API 키를 입력하면 대화를 시작할 수 있어요 🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# --------------------
# 세션 초기화
# --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "너는 게임 추천 전문 AI 챗봇이다. "
                "대화하듯 질문을 이어가며 사용자의 취향을 파악한다. "
                "최종적으로 2~3개의 게임을 추천하고, "
                "각 게임마다 추천 이유를 간단히 설명한다."
            )
        },
        {
            "role": "assistant",
            "content": "안녕하세요! 🎮 어떤 스타일의 게임을 찾고 계신가요?"
        }
    ]

# --------------------
# 기존 메시지 출력
# --------------------
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue

    bubble_class = "user" if msg["role"] == "user" else "assistant"

    with st.chat_message(msg["role"]):
        st.markdown(
            f"<div class='chat-bubble {bubble_class}'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

# --------------------
# 입력창
# --------------------
if prompt := st.chat_input("게임 취향을 자유롭게 말해 주세요"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(
            f"<div class='chat-bubble user'>{prompt}</div>",
            unsafe_allow_html=True
        )

    # --------------------
    # AI 응답 생성
    # --------------------
    with st.spinner("추천 중... 🎮"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )

    answer = response.choices[0].message.content
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(
            f"<div class='chat-bubble assistant'>{answer}</div>",
            unsafe_allow_html=True
        )
