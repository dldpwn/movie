import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="👻 맞춤형 호러 영화 추천소",
    page_icon="🎬",
    layout="centered"
)

# 타이틀 및 소개
st.title("👻 관객 맞춤형 호러 영화 추천소")
st.caption("함께 보는 사람, 공포 내성, 취향에 맞춰 딱 맞는 영화를 추천해 드립니다!")

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

style = st.multiselect(
    "🎭 선호하는 공포 스타일을 선택하세요 (복수 선택 가능)",
    ["심리/미스터리", "점프스케어(갑툭튀)", "오컬트/악마", "슬래셔/크리처", "잔잔한 힐링형/코미디"],
    default=["심리/미스터리"]
)

st.write("---")

# 2. 추천 로직 데이터
def get_recommendations(companion, tolerance, style):
    # 기본 추천 데이터베이스
    movies = []

    if companion == "가족" or tolerance == "입문자 (귀신 싫음)":
        movies.append({
            "title": "해피 데스데이 (Happy Death Day)",
            "genre": "코미디 / 미스터리 / 호러",
            "desc": "생일날 반복되는 죽음이라는 신선한 타임루프 소재! 무섭기보다는 스릴 있고 유쾌하게 즐길 수 있습니다.",
            "tag": "🎉 입문자 추천 & 무섭지 않은 호러"
        })
        movies.append({
            "title": "몬스터 호텔 (Hotel Transylvania)",
            "genre": "애니메이션 / 코미디",
            "desc": "귀여운 몬스터들이 총출동하는 애니메이션! 온 가족이 함께 웃으며 볼 수 있는 유쾌한 영화입니다.",
            "tag": "👨‍👩‍👧‍👦 가족 추천"
        })

    elif companion == "연인/데이트":
        movies.append({
            "title": "콰이어트 플레이스 (A Quiet Place)",
            "genre": "스릴러 / 서스펜스",
            "desc": "소리를 내면 공격하는 괴물들 속에서 살아남아야 하는 긴장감! 몰입감이 뛰어나 데이트용으로 제격입니다.",
            "tag": "👩‍❤️‍👨 데이트 추천 & 쫄깃한 긴장감"
        })
        movies.append({
            "title": "겟 아웃 (Get Out)",
            "genre": "미스터리 / 스릴러",
            "desc": "지루할 틈 없는 몰입감과 예측할 수 없는 반전! 관람 후 함께 이야기 나누기 아주 좋은 작품입니다.",
            "tag": "💡 심리 미스터리 띵작"
        })

    elif companion == "친구들과 다 같이":
        movies.append({
            "title": "곤지암 (Gonjiam: Haunted Asylum)",
            "genre": "파운드 푸티지 / 오컬트",
            "desc": "친구들과 불 끄고 모여서 보기 최적인 한국 체험형 공포 영화! 체감 공포도가 상당합니다.",
            "tag": "🍿 친구들과 떼관람 추천"
        })
        movies.append({
            "title": "캐빈 인 더 우즈 (The Cabin in the Woods)",
            "genre": "SF / 크리처 / 호러",
            "desc": "클리셰를 비틀어버리는 화려한 카타르시스! 친구들과 팝콘 먹으며 소리지르기 딱 좋습니다.",
            "tag": "🔥 화끈한 연출 & 유쾌함"
        })

    else: # 혼자 보는 경우
        if "상급 (진짜 무서운 것)" in tolerance or "마니아 (극강의 기괴함)" in tolerance:
            movies.append({
                "title": "유전 (Hereditary)",
                "genre": "오컬트 / 미스터리",
                "desc": "가장 압도적이고 숨 막히는 공포. 영화가 끝난 후에도 며칠 동안 잔상이 남는 극강의 오컬트 걸작입니다.",
                "tag": "💀 심야 혼자 보기 도전"
            })
            movies.append({
                "title": "랑종 (The Medium)",
                "genre": "페이크 다큐멘터리 / 오컬트",
                "desc": "태국 샤머니즘을 다룬 기괴하고 축축한 분위기의 공포. 기운이 꺾일 정도로 강렬한 체험을 선사합니다.",
                "tag": "🕯️ 극강의 마니아 추천"
            })
        else:
            movies.append({
                "title": "컨저링 (The Conjuring)",
                "genre": "오컬트 / 실화 바탕",
                "desc": "무서운 장면 없이 무서운 영화의 대명사! 정통 클래식 오컬트 공포의 진수를 느낄 수 있습니다.",
                "tag": "🕯️ 정통 명작 호러"
            })

    return movies

# 3. 결과 출력
if st.button("🎬 맞춤 영화 추천받기", use_container_width=True):
    results = get_recommendations(companion, tolerance, style)
    
    st.subheader(f"✨ [{companion}] 관객을 위한 맞춤 추천 영화")
    
    for idx, movie in enumerate(results, 1):
        with st.container():
            st.markdown(f"### {idx}. {movie['title']}")
            st.caption(f"🏷️ **태그:** {movie['tag']} | 🎭 **장르:** {movie['genre']}")
            st.write(movie['desc'])
            st.write("")
            
    st.balloons()

st.write("---")
st.caption("💡 팁: 영화를 보실 때는 불을 끄고 이어폰을 착용하시면 공포감이 2배가 됩니다!")
