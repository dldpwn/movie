import streamlit as st
from openai import OpenAI

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="AI 정보 선생님",
    page_icon="🤖"
)

st.title("🤖 친절한 AI 정보 선생님")
st.caption("궁금한 점이 있다면 무엇이든 물어보세요!")

# 2. 비밀 금고(secrets)에서 Gemini API 키 불러오기 및 OpenAI 클라이언트 설정
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
except Exception:
    st.error("🔑 API 키(GEMINI_API_KEY)를 찾을 수 없습니다. Secrets 설정을 확인해 주세요.")
    st.stop()

# 3. AI의 페르소나(성격 및 지침) 설정 (화면에 표시되지 않음)
system_prompt = {
    "role": "system",
    "content": "너는 중고등학생에게 설명하는 친절한 정보 선생님이야. 어려운 말은 쉬운 말로 바꿔 주고, 반드시 순수 한국어로만 답해."
}

# 4. 이전 대화 기록을 저장할 리스트(session_state) 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [system_prompt]

# 5. 이전 대화 화면에 출력하기 (system 메시지는 제외하고 user와 assistant 메시지만 표시)
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 6. 사용자 채팅 입력창 만들기
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자가 입력한 메시지를 화면에 말풍선으로 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 사용자의 메시지를 대화 기록 리스트에 추가
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # 7. AI의 답변 받기 및 실시간 스트리밍 출력
    with st.chat_message("assistant"):
        try:
            # API 요청 보내기 (이전 전체 대화 기록을 함께 전달하여 답변 문맥 유지)
            response_stream = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=st.session_state["messages"],
                stream=True
            )
            
            # 답변 글자가 실시간으로 흐르듯 출력되도록 st.write_stream 사용
            def stream_parser():
                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            full_response = st.write_stream(stream_parser())

            # 완성된 답변을 대화 기록 리스트에 추가하여 기억 유지
            st.session_state["messages"].append({"role": "assistant", "content": full_response})

        except Exception:
            # API 요청 실패 시 빨간색 시스템 오류 대신 친절한 한국어 안내 문구 표시
            st.info("💡 지금은 답변을 불러올 수 없습니다. 잠시 후 다시 시도해 주세요.")
