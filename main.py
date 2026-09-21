import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="👻 성격 & 취향 맞춤형 공포 영화 추천소",
    page_icon="🎬",
    layout="centered"
)

# 타이틀 및 소개
st.title("👻 성격 & 다중 취향 맞춤형 공포 영화 추천소")
st.caption("내 성격과 여러 선택 조건을 모두 분석하여 딱 맞는 영화를 추천해 드립니다!")

st.write("---")

# 1. 성격 및 관객 정보 입력
st.subheader("👤 1. 성격 및 관객 정보")
col1, col2 = st.columns(2)

with col1:
    personality = st.selectbox(
        "🧠 당신의 성격 유형은 어떤가요?",
        [
            "겁은 많지만 호기심이 왕성함",
            "이성적이고 분석적인 편",
            "스릴과 자극을 즐기는 에너자이저",
            "감수성이 풍부하고 몰입을 잘함",
            "평화주의자 (갑자기 놀라는 것 싫어함)"
        ]
    )

with col2:
    companion = st.selectbox(
        "👥 누구와 함께 보시나요?",
        ["혼자", "연인/데이트", "친구들과 다 같이", "가족"]
    )

# 2. 공포 내성 및 다중 장르 선택
st.subheader("🎭 2. 공포 내성 및 상세 취향 선택")

tolerance = st.select_slider(
    "😱 공포 내성 (공포 수준)",
    options=["입문자", "초보", "중급", "상급", "마니아"]
)

# 여러 개를 동시에 선택할 수 있는 multiselect
selected_genres = st.multiselect(
    "🎯 선호하는 공포 스타일을 모두 선택하세요 (복수 선택 가능)",
    [
        "슬래셔/살인마",
        "오컬트/악마/주술",
        "파운드 푸티지(실제 촬영 느낌)",
        "심리 스릴러/반전",
        "크리처/괴물",
        "호러 코미디/유쾌함"
    ],
    default=["심리 스릴러/반전"]
)

st.write("---")

# 3. 영화 데이터베이스 (장르 태그 복수 지정)
movies_db = [
    {
        "title": "겟 아웃 (Get Out)",
        "genres": ["심리 스릴러/반전"],
        "min_level": "초보",
        "desc": "기묘한 분위기와 예측할 수 없는 반전! 이성적이고 분석적인 성격의 관객에게 특히 높은 몰입감을 제공합니다.",
        "tag": "💡 반전 & 심리 스릴러"
    },
    {
        "title": "해피 데스데이 (Happy Death Day)",
        "genres": ["호러 코미디/유쾌함", "심리 스릴러/반전"],
        "min_level": "입문자",
        "desc": "생일날 반복되는 죽음이라는 타임루프 소재! 겁은 많지만 호기심이 많은 분들에게 부담 없는 스릴을 안겨줍니다.",
        "tag": "🎉 유쾌한 호러 & 타임루프"
    },
    {
        "title": "콰이어트 플레이스 (A Quiet Place)",
        "genres": ["크리처/괴물", "심리 스릴러/반전"],
        "min_level": "초보",
        "desc": "소리를 내면 공격하는 괴물과의 사투! 침묵 속 숨 막히는 긴장감이 감수성이 풍부한 관객을 사로잡습니다.",
        "tag": "🔇 긴장감 극대화 & 크리처"
    },
    {
        "title": "곤지암 (Gonjiam: Haunted Asylum)",
        "genres": ["파운드 푸티지(실제 촬영 느낌)", "오컬트/악마/주술"],
        "min_level": "상급",
        "desc": "폐병원 체험단을 생중계하는 듯한 현장감! 자극을 즐기는 관객이나 친구들과 모여서 보기 최적인 체험형 공포입니다.",
        "tag": "📹 체험형 공포 & 오컬트"
    },
    {
        "title": "유전 (Hereditary)",
        "genres": ["오컬트/악마/주술", "심리 스릴러/반전"],
        "min_level": "마니아",
        "desc": "가문에 내려진 저주와 기괴한 분위기. 영화가 끝난 후에도 잔상이 남는 압도적인 오컬트 심리 호러입니다.",
        "tag": "💀 극강의 오컬트 & 심리 압박"
    },
    {
        "title": "캐빈 인 더 우즈 (The Cabin in the Woods)",
        "genres": ["호러 코미디/유쾌함", "크리처/괴물", "슬래셔/살인마"],
        "min_level": "초보",
        "desc": "클리셰를 기발하게 비틀어버리는 호러 종합선물세트! 다양한 공포 요소를 한 번에 즐기고 싶을 때 제격입니다.",
        "tag": "🍿 호러 코미디 & 크리처 종합판"
    },
    {
        "title": "스크림 (Scream)",
        "genres": ["슬래셔/살인마", "심리 스릴러/반전"],
        "min_level": "중급",
        "desc": "가면을 쓴 살인마의 추적과 추리 요소가 결합된 명작! 범인을 분석하며 보기 좋습니다.",
        "tag": "🔪 정통 슬래셔 & 추리"
    }
]

# 4. 추천 로직 (선택한 조건을 포함하고 있는지 검사)
def recommend_movies(selected_genres, tolerance):
    matched_movies = []
    
    for movie in movies_db:
        # 선택한 장르 조건 중 하나 이상 포함하는지 확인 (복수 선택 반영)
        # 선택한 모든 장르를 포함하는 영화를 우선 검색
        has_genre_match = any(g in movie["genres"] for g in selected_genres)
        
        if has_genre_match:
            matched_movies.append(movie)
            
    return matched_movies

# 5. 결과 출력
if st.button("🎬 내 성격 & 취향에 맞는 영화 찾기", use_container_width=True):
    if not selected_genres:
        st.warning("⚠️ 최소 하나 이상의 공포 스타일을 선택해 주세요!")
    else:
        results = recommend_movies(selected_genres, tolerance)
        
        st.write("---")
        st.subheader(f"✨ [{personality}] 성격을 가진 관객을 위한 맞춤 영화")
        st.caption(f"선택하신 조건: **{', '.join(selected_genres)}** | 함께 보는 사람: **{companion}**")
        st.write("")
        
        if results:
            for idx, movie in enumerate(results, 1):
                with st.container():
                    st.markdown(f"### {idx}. {movie['title']}")
                    st.caption(f"🏷️ **태그:** {movie['tag']} | 🎭 **포함 장르:** {', '.join(movie['genres'])}")
                    st.write(movie['desc'])
                    st.write("")
            st.balloons()
        else:
            st.info("💡 선택하신 모든 조건 조합에 일치하는 영화를 찾지 못했습니다. 장르 선택 범위를 조금 더 넓혀보세요!")

st.write("---")
st.caption("💡 팁: 성격과 취향 조합에 맞는 영화를 관람하면 훨씬 더 깊은 몰입감을 얻을 수 있습니다.")
