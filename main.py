import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="👻 성격 & 취향 맞춤형 공포 영화 추천소",
    page_icon="🎬",
    layout="centered"
)

# 타이틀 및 소개
st.title("👻 성격 & 취향 맞춤형 공포 영화 추천소")
st.caption("공포 내성 단계(1~5단계)별로 완전히 차별화된 영화 중에서 성격과 상세 취향을 분석하여 추천합니다.")

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

# 내성 수준을 정수 점수로 매핑 (각 단계마다 서로 다른 전용 영화 배정)
tolerance_map = {
    "1단계: 입문자 (귀신/갑툭튀 절대 사절)": 1,
    "2단계: 초보 (적당한 긴장감 & 반전 위주)": 2,
    "3단계: 중급 (기본적인 슬래셔/스릴 가능)": 3,
    "4단계: 상급 (강한 오컬트 & 체험형 공포)": 4,
    "5단계: 마니아 (극강의 기괴함 & 하드코어)": 5
}

selected_tolerance_label = st.select_slider(
    "😱 공포 내성 (단계별 전용 영화 매칭)",
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

# 3. 영화 데이터베이스 (각 단계별로 중복 없이 완전히 다른 영화 배정)
movies_db = [
    # [1단계] 입문자 전용 (호러 코미디, 무자극)
    {
        "title": "몬스터 호텔 (Hotel Transylvania)",
        "genres": ["호러 코미디/유쾌함"],
        "level": 1,
        "level_name": "1단계 (입문자)",
        "desc": "귀여운 몬스터들이 총출동하는 애니메이션! 공포 요소가 없어 평화주의자나 극도로 겁이 많은 분께 추천합니다.",
        "tag": "🎉 무자극 호러 애니메이션"
    },
    {
        "title": "해피 데스데이 (Happy Death Day)",
        "genres": ["호러 코미디/유쾌함", "심리 스릴러/반전"],
        "level": 1,
        "level_name": "1단계 (입문자)",
        "desc": "생일날 반복되는 죽음이라는 타임루프 소재! 무섭기보다는 유쾌하고 스릴 넘쳐 호기심 많은 분께 딱입니다.",
        "tag": "🎉 유쾌한 타임루프 스릴러"
    },
    
    # [2단계] 초보 전용 (심리 스릴러, 잔혹함 적음)
    {
        "title": "겟 아웃 (Get Out)",
        "genres": ["심리 스릴러/반전"],
        "level": 2,
        "level_name": "2단계 (초보)",
        "desc": "기묘한 분위기와 예측할 수 없는 반전으로 끌고 갑니다. 분석적인 성격의 관객에게 강력 추천합니다.",
        "tag": "💡 반전 & 세련된 심리 스릴러"
    },
    {
        "title": "콰이어트 플레이스 (A Quiet Place)",
        "genres": ["크리처/괴물", "심리 스릴러/반전"],
        "level": 2,
        "level_name": "2단계 (초보)",
        "desc": "소리를 내면 공격하는 괴물과의 사투! 잔혹함보다는 서스펜스가 뛰어납니다.",
        "tag": "🔇 숨 막히는 서스펜스"
    },

    # [3단계] 중급 전용 (슬래셔, 클래식 호러)
    {
        "title": "스크림 (Scream)",
        "genres": ["슬래셔/살인마", "심리 스릴러/반전"],
        "level": 3,
        "level_name": "3단계 (중급)",
        "desc": "가면을 쓴 살인마의 추적과 범인 추리 요소가 결합된 슬래셔 명작입니다.",
        "tag": "🔪 정통 추리 슬래셔"
    },
    {
        "title": "캐빈 인 더 우즈 (The Cabin in the Woods)",
        "genres": ["호러 코미디/유쾌함", "크리처/괴물", "슬래셔/살인마"],
        "level": 3,
        "level_name": "3단계 (중급)",
        "desc": "클리셰를 기발하게 비틀어버리는 호러 종합선물세트! 친구들과 팝콘 먹으며 즐기기 좋은 스릴감입니다.",
        "tag": "🍿 화끈한 연출 & 호러 종합판"
    },

    # [4단계] 상급 전용 (강한 오컬트, 체험형)
    {
        "title": "곤지암 (Gonjiam: Haunted Asylum)",
        "genres": ["파운드 푸티지(실제 촬영 느낌)", "오컬트/악마/주술"],
        "level": 4,
        "level_name": "4단계 (상급)",
        "desc": "폐병원 체험단을 생중계하는 듯한 강렬한 현장감과 갑툭튀! 자극을 즐기는 관객에게 제격입니다.",
        "tag": "📹 체험형 극강 공포"
    },
    {
        "title": "컨저링 (The Conjuring)",
        "genres": ["오컬트/악마/주술"],
        "level": 4,
        "level_name": "4단계 (상급)",
        "desc": "실존 퇴마사 부부의 이야기를 다룬 명작! 무거운 분위기와 초자연 현상의 압박감이 상당합니다.",
        "tag": "🕯️ 정통 오컬트 명작"
    },

    # [5단계] 마니아 전용 (극강의 기괴함, 하드코어)
    {
        "title": "유전 (Hereditary)",
        "genres": ["오컬트/악마/주술", "심리 스릴러/반전"],
        "level": 5,
        "level_name": "5단계 (마니아)",
        "desc": "가문에 내려진 저주와 잔상이 남는 기괴함. 마니아들도 인정하는 압도적 수준의 오컬트 걸작입니다.",
        "tag": "💀 극강의 오컬트 & 정신적 압박"
    },
    {
        "title": "랑종 (The Medium)",
        "genres": ["오컬트/악마/주술", "파운드 푸티지(실제 촬영 느낌)"],
        "level": 5,
        "level_name": "5단계 (마니아)",
        "desc": "샤머니즘을 다룬 축축하고 기괴한 페이크 다큐멘터리! 멘탈이 강한 마니아에게만 권장하는 하드코어 호러입니다.",
        "tag": "🕯️ 하드코어 샤머니즘 호러"
    }
]

# 4. 단계별 엄격 분기 추천 로직
def recommend_strictly_by_level(selected_genres, user_level):
    # 정확히 해당 내성 단계(user_level)에 속한 영화만 1차 추출
    level_movies = [m for m in movies_db if m["level"] == user_level]
    
    # 그중 사용자가 선택한 취향(장르) 중 하나라도 만족하는 영화 필터링
    matched = []
    for movie in level_movies:
        if any(g in movie["genres"] for g in selected_genres):
            matched.append(movie)
            
    # 선택한 장르와 일치하는 영화가 없는 경우, 해당 내성 단계의 기본 영화 제공
    if not matched:
        matched = level_movies
        
    return matched

# 5. 결과 출력
if st.button("🎬 내 성격 & 단계에 맞는 영화 추천받기", use_container_width=True):
    if not selected_genres:
        st.warning("⚠️ 최소 하나 이상의 공포 스타일을 선택해 주세요!")
    else:
        results = recommend_strictly_by_level(selected_genres, user_level)
        
        st.write("---")
        st.subheader(f"✨ [{personality}] / [{selected_tolerance_label.split(':')[0]}] 맞춤 추천")
        st.caption(f"선택 장르: **{', '.join(selected_genres)}** | 함께 보는 사람: **{companion}**")
        st.write("")
        
        for idx, movie in enumerate(results, 1):
            with st.container():
                st.markdown(f"### {idx}. {movie['title']}")
                st.caption(f"🏷️ **태그:** {movie['tag']} | 😱 **전용 난이도:** {movie['level_name']}")
                st.write(movie['desc'])
                st.write("")
        st.balloons()

st.write("---")
st.caption("💡 팁: 각 공포 내성 단계별로 서로 다른 영화가 지정되어 안전하고 유쾌하게 관람할 수 있습니다.")
