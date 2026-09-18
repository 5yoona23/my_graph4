import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 제목
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 살펴봅니다."
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # genre에 여러 장르가 있으면 첫 번째 장르만 사용
    df["genre_first"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 총 관객수를 숫자로 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    )

    return df


df = load_data()


# ==================================================
# 첫 번째 그래프
# ==================================================

st.subheader("🍩 장르별 영화 편수")

genre_count = (
    df["genre_first"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["genre", "count"]

fig1 = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="none",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig1.update_layout(
    height=550,
    legend_title="장르"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("---")

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "장르별로 전체 영화에서 차지하는 편수와 비율이 어떻게 다른지 알 수 있습니다."
)


# ==================================================
# 두 번째 그래프
# ==================================================

st.markdown("---")

st.subheader("🌳 장르 안에 들어 있는 영화")

fig2 = px.treemap(
    df,
    path=["genre_first", "movieNm"],
    values="total_audi",
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=650
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("---")

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "장르 안에 어떤 영화들이 포함되어 있고, 영화별 총 관객 규모가 어떻게 다른지 알 수 있습니다."
)
