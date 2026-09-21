import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="👻 맞춤형 공포 영화 추천소",
    page_icon="🎬",
    layout="centered"
)

# 타이틀 및 소개
st.title("👻 취향별 & 관객별 공포 영화 추천소")
st.caption("공포 영화의 다양한 세부 장르와 관객의 특성에 맞춰 딱 맞는 영화를 추천해 드립니다!")

st.write("---")

# 1. 사용자 입력 받기
col1, col2 = st.columns(2)

with col1:
    companion = st.selectbox(
        "👥 누구와 함께 보시나요?",
        ["혼자", "연인/데이트", "친구들과 다 같이", "가족"]
    )

with col2:
    tolerance = st.select_slider(
        "😱 공포 내성 (공포 수준)",
        options=["입문자 (귀신 싫음)", "초보 (적당한 으스스함)", "중급 (갑툭튀 가능)", "상급 (진짜 무서운 것)", "마니아 (극강의 기괴함)"]
    )

genre_choice = st.selectbox(
    "🎭 가장 끌리는 공포 영화 장르를 선택하세요",
    [
        "전체 (알아서 추천)",
        "🔪 슬래셔 / 킬러 (살인마, 긴장감)",
        "🕯️ 오컬트 / 악마 / 퇴마 (주술, 초자연)",
        "📹 파운드 푸티지 / 리얼리티 (실제 촬영 느낌)",
        "🧠 심리 스릴러 / 미스터리 (반전, 정신적 압박)",
        "👹 크리처 / 괴물 / 바이러스 (괴물, 감염)",
        "🎃 호러 코미디 / 액션 (유쾌함, 덜 무서움)"
    ]
)

st.write("---")

# 2. 장르별 영화 데이터베이스
movie_db = {
    "슬래셔": [
        {"title": "스크림 (Scream)", "desc": "가면을 쓴 살인마의 추적! 슬래셔 장르의 대표적인 명작입니다.", "level": "중급", "tag": "🔪 정통 슬래셔"},
        {"title": "텍사스 전기톱 연쇄살인사건", "desc": "숨 막히는 추격전과 잔혹한 긴장감이 특징인 고전 슬래셔 영화입니다.", "level": "상급", "tag": "🩸 하드코어 슬래셔"}
    ],
    "오컬트": [
        {"title": "컨저링 (The Conjuring)", "desc": "실존 퇴마사 부부의 이야기를 다룬 정통 오컬트 명작입니다.", "level": "중급", "tag": "🕯️ 초자연 현상"},
        {"title": "유전 (Hereditary)", "desc": "가족에게 내려진 기괴한 저주와 압도적인 오컬트 분위기를 자랑합니다.", "level": "마니아", "tag": "💀 심리적 압박 & 오컬트"},
        {"title": "파묘 (Exhuma)", "desc": "수상한 묘를 이장하면서 벌어지는 한국형 오컬트 스릴러입니다.", "level": "초보", "tag": "🇰🇷 한국형 오컬트"}
    ],
    "파운드 푸티지": [
        {"title": "곤지암", "desc": "폐병원 체험단을 생중계하는 듯한 몰입감을 주는 카메라 연출이 특징입니다.", "level": "상급", "tag": "📹 한국 체험형 공포"},
        {"title": "블레어 윗치 (The Blair Witch Project)", "desc": "핸드헬드 카메라 연출의 원조로, 실제 사건 같은 스릴을 줍니다.", "level": "중급", "tag": "🌲 리얼리티 공포"}
    ],
    "심리 스릴러": [
        {"title": "겟 아웃 (Get Out)", "desc": "기묘한 분위기와 인종적 소재를 결합한 세련된 반전 스릴러입니다.", "level": "초보", "tag": "💡 반전 & 심리 압박"},
        {"title": "미드소마 (Midsommar)", "desc": "밝은 대낮의 축제 속에서 펼쳐지는 기괴하고 기이한 심리 호러입니다.", "level": "상급", "tag": "☀️ 백야 호러"}
    ],
    "크리처": [
        {"title": "콰이어트 플레이스 (A Quiet Place)", "desc": "소리를 내는 순간 공격받는 괴물들과의 숨 막히는 생존기입니다.", "level": "초보", "tag": "🔇 긴장감 극대화"},
        {"title": "더 씽 (The Thing)", "desc": "남극 기지에서 벌어지는 정체불명의 외계 생물체와의 사투를 다룹니다.", "level": "중급", "tag": "👾 클래식 크리처"}
    ],
    "호러 코미디": [
        {"title": "해피 데스데이 (Happy Death Day)", "desc": "타임루프 소재와 유쾌한 전개가 돋보이는 입문용 공포 영화입니다.", "level": "입문자", "tag": "🎉 유쾌한 호러"},
        {"title": "캐빈 인 더 우즈 (The Cabin in the Woods)", "desc": "공포 영화의 클리셰를 기발하게 비틀어버리는 재미가 있습니다.", "level": "초보", "tag": "🍿 팝콘 무비"}
    ]
}

# 3. 추천 로직
def get_recommendations(selected_genre, tolerance):
    recommendations = []
    
    # 장르 필터링
    target_genres = []
    if "슬래셔" in selected_genre:
        target_genres.append("슬래셔")
    elif "오컬트" in selected_genre:
        target_genres.append("오컬트")
    elif "파운드 푸티지" in selected_genre:
        target_genres.append("파운드 푸티지")
    elif "심리 스릴러" in selected_genre:
        target_genres.append("심리 스릴러")
    elif "크리처" in selected_genre:
        target_genres.append("크리처")
    elif "호러 코미디" in selected_genre:
        target_genres.append("호러 코미디")
    else:
        # 전체 선택 시 주요 장르에서 하나씩 추출
        target_genres = list(movie_db.keys())

    for g in target_genres:
        for movie in movie_db[g]:
            recommendations.append(movie)

    return recommendations

# 4. 결과 출력
if st.button("🎬 맞춤 영화 추천받기", use_container_width=True):
    results = get_recommendations(genre_choice, tolerance)
    
    st.subheader(f"✨ [{companion}] 관객을 위한 맞춤 추천 목록")
    
    if results:
        for idx, movie in enumerate(results, 1):
            with st.container():
                st.markdown(f"### {idx}. {movie['title']}")
                st.caption(f"🏷️ **태그:** {movie['tag']} | 😱 **추천 난이도:** {movie['level']}")
                st.write(movie['desc'])
                st.write("")
    st.balloons()

st.write("---")
st.caption("💡 Tip: 영화 장르별 특성에 맞춰 조명이나 음향 환경을 조절하시면 더 재밌게 관람하실 수 있습니다!")
