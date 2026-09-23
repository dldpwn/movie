import streamlit as st
from openai import OpenAI

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="AI 대화방",
    page_icon="🐶"
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

# 3. 사이드바 - 캐릭터별 성격 지침 정의
tone_prompts = {
    "🐶 보이넥스트도어 명재현": (
        "너는 보이넥스트도어(BOYNEXTDOOR)의 리더 명재현이야. "
        "상대방을 친근하고 다정하게 대하며, 에너지 넘치고 댕댕이(강아지) 같은 에너지를 발산해줘. "
        "주요 말투 및 성격 특징:\n"
        "- 반말을 기본으로 사용하되, 상대를 진심으로 아끼고 응원하는 따뜻한 톤을 유지해.\n"
        "- '진짜로!', '솔직히 말하면', '~했잖아!', '~인 거 알지?', '대박이다' 같은 표현을 자주 써.\n"
        "- 리액션이 풍부하고, 이모티콘(🐶, ✨, 💙, 🔥)을 자주 활용해.\n"
        "- 음악, 무대, 그리고 상대방(팬/친구)에 대한 사랑과 열정이 넘치는 멘트를 해줘.\n"
        "- 무조건 순수 한국어로만 답변해줘."
    ),
    "친절한 선생님": "너는 중고등학생에게 설명하는 친절한 정보 선생님이야. 어려운 말은 쉬운 말로 바꿔 주고, 따뜻하고 친절하게 순수 한국어로만 답해.",
    "시크한 전문가": "너는 핵심만 명확하게 짚어주는 시크하고 간결한 정보 기술 전문가야. 쓸데없는 군더더기 없이 전문적이고 세련된 한국어로 답해.",
    "되물어보는 조교": "너는 학생이 스스로 생각하도록 돕는 정보 수업 조교야. 정답을 바로 알려주지 말고 힌트를 하나 준 뒤 질문을 던져. 학생이 정답을 말했을 때만 비로소 정답을 확인해 주고 칭찬해 줘. 반드시 한국어로만 답해."
}

# 4. 사이드바 - 설정 메뉴 구성
with st.sidebar:
    st.header("⚙️ AI 캐릭터 설정")
    
    # 캐릭터 선택 시 대화 기록 자동 리셋하는 함수
    def reset_chat_on_change():
        st.session_state["messages"] = []

    tone_choice = st.radio(
        "🎭 AI 말투/캐릭터 고르기",
        list(tone_prompts.keys()),
        index=0,
        on_change=reset_chat_on_change
    )
    
    # 성격 문장 직접 수정할 수 있는 입력창
    system_instruction = st.text_area(
        "✍️ AI 성격 지침 (직접 수정 가능)",
        value=tone_prompts[tone_choice],
        height=180
    )
    
    st.write("---")
    
    # 대화 지우기 버튼
    if st.button("🗑️ 대화 기록 지우기", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# 5. 메인 화면 타이틀
st.title("💬 AI 대화하기")
st.caption(f"현재 캐릭터: **{tone_choice}**")

# 6. 이전 대화 기록 저장용 session_state 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 7. 이전 대화 화면에 출력하기
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 8. 사용자 채팅 입력창 처리
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자가 입력한 메시지를 화면에 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # 최신 성격 지침(System Prompt)을 항상 첫 번째에 삽입
    messages_for_api = [{"role": "system", "content": system_instruction}] + st.session_state["messages"]

    # 9. AI 답변 생성 및 스트리밍
    with st.chat_message("assistant"):
        try:
            response_stream = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages_for_api,
                stream=True
            )
            
            def stream_parser():
                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            full_response = st.write_stream(stream_parser())
            st.session_state["messages"].append({"role": "assistant", "content": full_response})

        except Exception:
            st.info("💡 지금은 답변을 불러올 수 없습니다. 잠시 후 다시 시도해 주세요.")
