import datetime
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

# 1. 페이지 기본 설정 (타이틀, 파비콘, 레이아웃)
st.set_page_config(
    page_title="어제 박스오피스 순위",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 어제 일별 박스오피스")
st.caption("영화진흥위원회(KOBIS) API를 활용한 실시간 데이터 시각화")

# 2. 한국 시간(KST, UTC+9) 기준 어제 날짜 계산
# 서버 시계가 해외 기준(UTC)일 수 있으므로 타임존을 한국 시간으로 맞춥니다.
kst_timezone = datetime.timezone(datetime.timedelta(hours=9))
today_kst = datetime.datetime.now(kst_timezone).date()
yesterday = today_kst - datetime.timedelta(days=1)

# API 요청에 필요한 YYYYMMDD 형태 문자열 생성
target_date_str = yesterday.strftime("%Y%m%d")
formatted_date_display = yesterday.strftime("%Y년 %m월 %d일")

st.write(f"📅 **조회 일자:** {formatted_date_display}")

# 3. Streamlit Secrets에서 API 인증키 불러오기
# Streamlit Cloud의 Secrets에 KOBIS_KEY가 설정되어 있어야 합니다.
try:
    api_key = st.secrets["KOBIS_KEY"]
except Exception:
    api_key = None

# 인증키가 없을 때 안내 메시지
if not api_key:
    st.error("🔑 API 인증키(KOBIS_KEY)를 찾을 수 없습니다.")
    st.info("""
    **확인 조치 사항:**
    1. Streamlit Cloud의 앱 설정 내 **Secrets** 메뉴로 이동하세요.
    2. `KOBIS_KEY = "발급받은_인증키"` 형태로 키를 등록했는지 확인해 주세요.
    """)
    st.stop()

# 4. KOBIS API 데이터 요청
api_url = "https://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
params = {
    "key": api_key,
    "targetDt": target_date_str
}

try:
    response = requests.get(api_url, params=params, timeout=10)
    data = response.json()
except Exception as e:
    st.error("📡 API 서버와의 통신 중 오류가 발생했습니다.")
    st.caption(f"상세 오류 내용: {e}")
    st.stop()

# 5. API 응답 에러 및 예외 처리
# KOBIS API는 인증키가 틀려도 200 OK와 함께 faultInfo 객체를 반환합니다.
if "faultInfo" in data:
    fault_msg = data["faultInfo"].get("message", "인증키 문제로 오류가 발생했습니다.")
    st.error(f"❌ KOBIS API 오류 발생: {fault_msg}")
    st.info("등록된 API 인증키가 올바른지 확인해 주세요.")
    st.stop()

# 응답 내 박스오피스 목록 추출
box_office_result = data.get("boxOfficeResult", {})
daily_list = box_office_result.get("dailyBoxOfficeList", [])

# 영화 목록이 비어 있는 경우 예외 처리
if not daily_list:
    st.warning("⚠️ 해당 날짜의 박스오피스 데이터가 존재하지 않거나 집계 중입니다.")
    st.info("KOBIS API 집계 현황 또는 조회 날짜를 확인해 주세요.")
    st.stop()

# 6. 데이터 전처리
df = pd.DataFrame(daily_list)

# 문자열 데이터를 숫자형(int)으로 변환
numeric_cols = ["rank", "rankInten", "audiCnt", "audiAcc", "scrnCnt", "showCnt"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# 7. 1위 영화 지표 카드(Metric) 표시
st.write("---")
top_movie = df[df["rank"] == 1].iloc[0]

st.subheader(f"🥇 1위 영화: {top_movie['movieNm']}")

col1, col2, col3 = st.columns(3)

with col1:
    # 당일 관객수
    st.metric(
        label="어제 관객수",
        value=f"{top_movie['audiCnt']:,} 명"
    )

with col2:
    # 누적 관객수
    st.metric(
        label="누적 관객수",
        value=f"{top_movie['audiAcc']:,} 명"
    )

with col3:
    # 스크린수
    st.metric(
        label="스크린수",
        value=f"{top_movie['scrnCnt']:,} 개"
    )

st.write("---")

# 8. 관객수 상위 5편 막대그래프
st.subheader("📊 관객수 상위 5개 영화")

top5_df = df.sort_values(by="rank").head(5).copy()

# 시각화용 차트 생성
fig = px.bar(
    top5_df,
    x="movieNm",
    y="audiCnt",
    text="audiCnt",
    labels={"movieNm": "영화명", "audiCnt": "관객수(명)"},
    title="어제 일별 관객수 Top 5"
)

# 그래프 레이아웃 및 값 표시 형식 설정
fig.update_traces(
    texttemplate="%{text:,}명",
    textposition="outside"
)
fig.update_layout(
    xaxis_title=None,
    yaxis_title="관객수 (명)",
    height=450,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.write("---")

# 9. 전체 박스오피스 순위 표
st.subheader("📋 전체 박스오피스 순위")

# 표에 출력할 열선택 및 이름 변경
display_df = df[[
    "rank", "movieNm", "openDt", "audiCnt", "audiAcc", "scrnCnt"
]].copy()

display_df.columns = [
    "순위", "영화명", "개봉일", "어제 관객수", "누적 관객수", "스크린수"
]

# 숫자 포맷 변경 (천 단위 쉼표 표기)
st.dataframe(
    display_df,
    column_config={
        "어제 관객수": st.column_config.NumberColumn(format="%d 명"),
        "누적 관객수": st.column_config.NumberColumn(format="%d 명"),
        "스크린수": st.column_config.NumberColumn(format="%d 개"),
    },
    use_container_width=True,
    hide_index=True
)
