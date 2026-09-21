import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="👻 성격 & 취향 맞춤형 공포 영화 추천소",
    page_icon="🎬",
    layout="centered"
)

# 타이틀 및 소개
st.title("👻 성격 & 취향 맞춤형 공포 영화 추천소")
st.caption("공포 내성 난이도와 성격, 복수 선택한 취향을 엄격히 분석하여 최적의 영화를 추천합니다.")

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

# 내성 수준을 정수 점수로 매핑 (입문자:1, 초보:2, 중급:3, 상급:4, 마니아:5)
tolerance_map = {
    "입문자 (귀신 싫음/호러 코미디만)": 1,
    "초보 (적당한 스릴/반전 위주)": 2,
    "중급 (기본적인 갑툭튀/슬래셔 가능)": 3,
    "상급 (진짜 무서운 오컬트/체험형)": 4,
    "마니아 (극강의 기괴함/하드코어)": 5
}

selected_tolerance_label = st.select_slider(
    "😱 공포 내성 (단계별 맞춤 필터링)",
    options=list(tolerance_map.keys())
)
user_level = tolerance_map[selected_tolerance_label]

selected_genres = st.multiselect(
    "🎯 선호하는 공포 스타일을 선택하세요 (복수 선택 가능)",
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

# 3. 영화 데이터베이스 (각 영화마다 명확한 난이도 level 지정)
# level 1: 입문자, 2: 초보, 3: 중급, 4: 상급, 5: 마니아
movies_db = [
    # Level 1 (입문자 전용)
    {
        "title": "몬스터 호텔 (Hotel Transylvania)",
        "genres": ["호러 코미디/유쾌함"],
        "level": 1,
        "level_name": "입문자",
        "desc": "귀여운 몬스터들이 총출동하는 유쾌한 애니메이션! 공포 요소가 전혀 없어 평화주의자나 극도로 겁이 많은 분께 추천합니다.",
        "tag": "🎉 완전 무자극 & 가족/입문자"
    },
    {
        "title": "해피 데스데이 (Happy Death Day)",
        "genres": ["호러 코미디/유쾌함", "심리 스릴러/반전"],
        "level": 1,
        "level_name": "입문자",
        "desc": "생일날 반복되는 죽음이라는 타임루프 소재! 무섭기보다는 유쾌하고 스릴 넘쳐 겁은 많지만 호기심이 많은 관객에게 딱입니다.",
        "tag": "🎉 유쾌한 호러 & 타임루프"
    },
    
    # Level 2 (초보용)
    {
        "title": "겟 아웃 (Get Out)",
        "genres": ["심리 스릴러/반전"],
        "level": 2,
        "level_name": "초보",
        "desc": "귀신이나 갑툭튀 없이 기묘한 분위기와 예측할 수 없는 반전으로 끌고 갑니다. 분석적인 성격의 관객에게 강력 추천합니다.",
        "tag": "💡 세련된 반전 & 심리 스릴러"
    },
    {
        "title": "콰이어트 플레이스 (A Quiet Place)",
        "genres": ["크리처/괴물", "심리 스릴러/반전"],
        "level": 2,
        "level_name": "초보",
        "desc": "소리를 내면 공격하는 괴물과의 숨 막히는 사투! 잔혹함보다는 서스펜스가 뛰어나 연인이나 데이트용으로 좋습니다.",
        "tag": "🔇 몰입감 극대화 & 크리처"
    },

    # Level 3 (중급용)
    {
        "title": "스크림 (Scream)",
        "genres": ["슬래셔/살인마", "심리 스릴러/반전"],
        "level": 3,
        "level_name": "중급",
        "desc": "가면을 쓴 살인마의 추적과 추리 요소가 결합된 정통 슬래셔! 적당한 긴장감과 추리를 동시에 즐길 수 있습니다.",
        "tag": "🔪 정통 슬래셔 & 추리"
    },
    {
        "title": "캐빈 인 더 우즈 (The Cabin in the Woods)",
        "genres": ["호러 코미디/유쾌함", "크리처/괴물", "슬래셔/살인마"],
        "level": 3,
        "level_name": "중급",
        "desc": "클리셰를 기발하게 비틀어버리는 호러 종합선물세트! 친구들과 모여 팝콘을 먹으며 즐기기 좋은 스릴감입니다.",
        "tag": "🍿 화끈한 연출 & 호러 종합판"
    },

    # Level 4 (상급용)
    {
        "title": "곤지암 (Gonjiam: Haunted Asylum)",
        "genres": ["파운드 푸티지(실제 촬영 느낌)", "오컬트/악마/주술"],
        "level": 4,
        "level_name": "상급",
        "desc": "폐병원 체험단을 생중계하는 듯한 강렬한 현장감과 갑툭튀! 자극과 체험형 공포를 즐기는 관객에게 제격입니다.",
        "tag": "📹 체험형 극강 공포"
    },
    {
        "title": "컨저링 (The Conjuring)",
        "genres": ["오컬트/악마/주술"],
        "level": 4,
        "level_name": "상급",
        "desc": "실존 퇴마사 부부의 이야기를 다룬 정통 오컬트 명작! 무거운 분위기와 초자연 현상이 주는 압박감이 상당합니다.",
        "tag": "🕯️ 정통 오컬트 명작"
    },

    # Level 5 (마니아용)
    {
        "title": "유전 (Hereditary)",
        "genres": ["오컬트/악마/주술", "심리 스릴러/반전"],
        "level": 5,
        "level_name": "마니아",
        "desc": "가문에 내려진 저주와 며칠 동안 잔상이 남는 기괴함. 공포 영화 마니아들도 인정하는 압도적 수준의 오컬트 걸작입니다.",
        "tag": "💀 극강의 오컬트 & 정신적 압박"
    },
    {
        "title": "랑종 (The Medium)",
        "genres": ["오컬트/악마/주술", "파운드 푸티지(실제 촬영 느낌)"],
        "level": 5,
        "level_name": "마니아",
        "desc": "샤머니즘을 다룬 축축하고 기괴한 페이크 다큐멘터리! 멘탈이 강한 마니아 관객에게만 권장하는 극강의 공포입니다.",
        "tag": "🕯️ 마니아 전용 극강 호러"
    }
]

# 4. 엄격한 필터링 로직
def recommend_strict_movies(selected_genres, user_level):
    matched = []
    
    for movie in movies_db:
        # 1) 내성 수준 일치 여부 확인 (사용자가 선택한 레벨과 같거나 ±1 범위 내로 제한)
        # 입문자(1)에게 상급/마니아(4~5) 영화가 추천되는 것을 완벽 차단
        level_diff = abs(movie["level"] - user_level)
        
        # 2) 장르 조건 포함 여부 확인
        has_genre = any(g in movie["genres"] for g in selected_genres)
        
        # 내성이 딱 맞고 장르도 부합하는 영화 필터링
        if level_diff <= 1 and has_genre:
            matched.append(movie)
            
    # 난이도가 사용자 레벨에 가장 정확히 일치하는 순으로 정렬
    matched.sort(key=lambda x: abs(x["level"] - user_level))
    return matched

# 5. 결과 출력
if st.button("🎬 내 성격 & 내성에 맞는 영화 추천받기", use_container_width=True):
    if not selected_genres:
        st.warning("⚠️ 최소 하나 이상의 공포 스타일을 선택해 주세요!")
    else:
        results = recommend_strict_movies(selected_genres, user_level)
        
        st.write("---")
        st.subheader(f"✨ [{personality}] / [{selected_tolerance_label.split(' ')[0]}] 맞춤 추천")
        st.caption(f"선택 장르: **{', '.join(selected_genres)}** | 함께 보는 사람: **{companion}**")
        st.write("")
        
        if results:
            for idx, movie in enumerate(results, 1):
                with st.container():
                    st.markdown(f"### {idx}. {movie['title']}")
                    st.caption(f"🏷️ **태그:** {movie['tag']} | 😱 **난이도:** {movie['level_name']} (Lv.{movie['level']})")
                    st.write(movie['desc'])
                    st.write("")
            st.balloons()
        else:
            st.info("💡 선택하신 공포 내성 단계와 장르 조합에 맞는 영화가 없습니다. 장르 선택을 조정해 보세요!")

st.write("---")
st.caption("💡 팁: 내성 단계에 꼭 맞는 영화를 선택하셔야 유쾌한 감상이 가능합니다.")
