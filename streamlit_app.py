import streamlit as st
from openai import OpenAI

# 제목과 설명
st.title("🎮 게임 추천 AI 챗봇")
st.write(
    "당신의 취향에 맞는 게임을 추천해주는 AI 챗봇입니다.\n\n"
    "선호하는 장르, 플랫폼(PC / 콘솔 / 모바일), "
    "혼자 또는 친구와 플레이 여부 등을 입력해 주세요.\n\n"
    "예시: *스토리 위주의 싱글 플레이 PC 게임 추천해줘*"
)

# OpenAI API 키 입력
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 게임 추천 전문 AI 챗봇이다. "
                    "사용자의 취향, 플레이 스타일, 플랫폼, "
                    "난이도 선호, 혼자/멀티 여부를 고려해 "
                    "이유와 함께 게임을 추천해야 한다. "
                    "추천은 2~4개 정도로 간결하게 제시한다."
                )
            }
        ]

    # 기존 메시지 출력 (system 메시지는 숨김)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("어떤 게임을 찾고 계신가요?"):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API 호출
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # 응답 스트리밍 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
