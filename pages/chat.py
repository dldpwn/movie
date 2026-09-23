import streamlit as st
from openai import OpenAI

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="AI 정보 선생님",
    page_icon="🤖"
)

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

# 3. 사이드바 - 설정 메뉴 구성
with st.sidebar:
    st.header("⚙️ AI 설정")
    
    # 3-1. 말투 고르기
    tone_choice = st.radio(
        "🎭 AI 말투 고르기",
        ["친절한 선생님", "시크한 전문가", "되물어보는 조교"],
        index=0
    )
    
    # 선택된 말투별 기본 성격 지침 정의
    tone_prompts = {
        "친절한 선생님": "너는 중고등학생에게 설명하는 친절한 정보 선생님이야. 어려운 말은 쉬운 말로 바꿔 주고, 따뜻하고 친절하게 순수 한국어로만 답해.",
        "시크한 전문가": "너는 핵심만 명확하게 짚어주는 시크하고 간결한 정보 기술 전문가야. 쓸데없는 군더더기 없이 전문적이고 세련된 한국어로 답해.",
        "되물어보는 조교": "너는 학생이 스스로 생각하도록 돕는 정보 수업 조교야. 정답을 바로 알려주지 말고 힌트를 하나 준 뒤 질문을 던져. 학생이 정답을 말했을 때만 비로소 정답을 확인해 주고 칭찬해 줘. 반드시 한국어로만 답해."
    }
    
    # 3-2. 성격 문장 직접 수정할 수 있는 입력창
    system_instruction = st.text_area(
        "✍️ AI 성격 지침 (직접 수정 가능)",
        value=tone_prompts[tone_choice],
        height=150
    )
    
    st.write("---")
    
    # 3-3. 대화 지우기 버튼
    if st.button("🗑️ 대화 기록 지우기", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# 4. 메인 화면 타이틀
st.title("🤖 AI 정보 선생님")
st.caption(f"현재 설정된 말투: **{tone_choice}**")

# 5. 이전 대화 기록 저장용 session_state 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 6. 이전 대화 화면에 출력하기 (메시지 전송 기록만 표시)
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. 사용자 채팅 입력창 처리
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자가 입력한 메시지를 화면에 말풍선으로 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 사용자 메시지를 대화 기록 리스트에 추가
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # 8. API 요청에 보낼 전체 메시지 구성
    # 사이드바에서 고른 최신 성격 지침을 첫 번째(system) 메시지로 동적 배치하여 바로 반영되게 함
    messages_for_api = [{"role": "system", "content": system_instruction}] + st.session_state["messages"]

    # 9. AI의 답변 받기 및 실시간 스트리밍 출력
    with st.chat_message("assistant"):
        try:
            response_stream = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages_for_api,
                stream=True
            )
            
            # 답변 글자가 실시간으로 흐르듯 출력되도록 조각(chunk) 처리
            def stream_parser():
                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            full_response = st.write_stream(stream_parser())

            # 완성된 AI 답변을 대화 기록 리스트에 추가하여 맥락 유지
            st.session_state["messages"].append({"role": "assistant", "content": full_response})

        except Exception:
            # 오류 발생 시 빨간 오류 화면 대신 친절한 한국어 안내 문구 표시
            st.info("💡 지금은 답변을 불러올 수 없습니다. 잠시 후 다시 시도해 주세요.")
