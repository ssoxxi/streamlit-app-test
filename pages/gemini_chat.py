import streamlit as st
from google import genai
from google.genai import types

st.header("💬 Gemini 챗봇")

# API 키 확인
try:
    api_key = st.secrets["gemini"]["GEMINI_API_KEY"]
    if api_key == "your-api-key-here":
        st.warning("⚠️ .streamlit/secrets.toml에서 GEMINI_API_KEY를 설정하세요!")
        st.stop()
except Exception:
    st.error("API 키를 찾을 수 없습니다. .streamlit/secrets.toml 파일을 확인하세요.")
    st.stop()

# 설정 로드 (secrets.toml에서)
gemini_model = st.secrets["gemini"]["model"]
temperature = st.secrets["gemini"]["temperature"]

# 클라이언트 초기화 (캐싱하여 재사용)
@st.cache_resource
def get_client(_api_key):
    return genai.Client(api_key=_api_key)

client = get_client(api_key)

# 생성 설정
generation_config = types.GenerateContentConfig(
    temperature=temperature,
)

# 세션 상태 초기화 (사용자별 채팅 세션)
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model=gemini_model, config=generation_config)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 초기화 버튼
if st.button("대화 초기화"):
    st.session_state.chat = client.chats.create(model=gemini_model, config=generation_config)
    st.session_state.messages = []
    st.rerun()

# 채팅 UI
# 메시지 컨테이너 (고정 높이, 스크롤 가능)
chat_container = st.container(height=800)

# 이전 메시지 표시
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 사용자 입력 (컨테이너 밖 = 항상 아래에 고정)
prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    # 사용자 메시지 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 (스트리밍)
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in st.session_state.chat.send_message_stream(prompt):
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response)

            response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
