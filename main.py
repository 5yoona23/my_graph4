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

# ==================================================
# 세 번째 그래프
# ==================================================

st.markdown("---")

st.subheader("📊 총 관객수 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객수 분포",
    labels={
        "total_audi": "총 관객수",
        "count": "영화 편수"
    }
)

fig3.update_layout(
    height=550,
    xaxis_title="총 관객수",
    yaxis_title="영화 편수"
)

fig3.update_traces(
    hovertemplate=(
        "총 관객수 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# --------------------------------------------------
# 히스토그램에서 알 수 있는 내용
# --------------------------------------------------

# 가장 관객이 많은 영화 찾기
max_audi_row = df.loc[df["total_audi"].idxmax()]

max_movie = max_audi_row["movieNm"]
max_audi = int(max_audi_row["total_audi"])

# 영화가 가장 많이 몰려 있는 구간 계산
counts, bins = pd.cut(
    df["total_audi"],
    bins=20,
    include_lowest=True,
    retbins=True
).value_counts().sort_index(), None

most_common_bin = counts.idxmax()

st.markdown("---")

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    f"대부분의 영화는 **{most_common_bin.left:,.0f}명 ~ "
    f"{most_common_bin.right:,.0f}명** 구간에 몰려 있습니다. "
    f"가장 관객이 많은 영화는 **{max_movie}**으로, "
    f"총 **{max_audi:,}명**의 관객을 기록했습니다."
)

# ==================================================
# 네 번째 그래프
# ==================================================

st.markdown("---")

st.subheader("🔵 개봉일 스크린수와 총 관객의 관계")

# 산점도에 사용할 데이터
scatter_df = df.dropna(
    subset=["first_scrn", "total_audi", "movieNm", "genre_first"]
).copy()

# 숫자형으로 변환
scatter_df["first_scrn"] = pd.to_numeric(
    scatter_df["first_scrn"],
    errors="coerce"
)

scatter_df["total_audi"] = pd.to_numeric(
    scatter_df["total_audi"],
    errors="coerce"
)

scatter_df = scatter_df.dropna(
    subset=["first_scrn", "total_audi"]
)

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre_first",
    hover_name="movieNm",
    hover_data={
        "first_scrn": ":,",
        "total_audi": ":,",
        "genre_first": True
    },
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "genre_first": "장르"
    },
    title="개봉일 스크린수와 총 관객의 관계"
)

fig4.update_traces(
    marker=dict(
        size=9,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객수: %{y:,}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    height=650,
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객수",
    legend_title="장르"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# 그래프 설명 구역
st.markdown("---")

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "개봉일 스크린수와 총 관객수 사이의 관계를 살펴보고, "
    "장르에 따라 영화들이 어떻게 분포하는지 비교할 수 있습니다."
)

# ==================================================
# 다섯 번째 그래프
# ==================================================

st.markdown("---")

st.subheader("📦 장르별 총 관객수 분포")

# 장르별 영화 편수 계산
genre_counts = (
    df["genre_first"]
    .value_counts()
)

# 영화가 10편 이상인 장르만 선택
valid_genres = genre_counts[
    genre_counts >= 10
].index

box_df = df[
    df["genre_first"].isin(valid_genres)
].copy()

# 숫자형 변환
box_df["total_audi"] = pd.to_numeric(
    box_df["total_audi"],
    errors="coerce"
)

box_df = box_df.dropna(
    subset=["total_audi"]
)

# 박스플롯
fig5 = px.box(
    box_df,
    x="genre_first",
    y="total_audi",
    color="genre_first",
    points="outliers",
    hover_name="movieNm",
    labels={
        "genre_first": "장르",
        "total_audi": "총 관객수"
    },
    title="영화가 10편 이상인 장르의 총 관객수 분포"
)

# 이상치에 마우스를 올렸을 때 영화명이 보이도록 설정
fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객수: %{y:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=650,
    xaxis_title="장르",
    yaxis_title="총 관객수",
    showlegend=False
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# 그래프 설명 구역
st.markdown("---")

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "영화가 10편 이상인 장르끼리 총 관객수의 중앙값과 분포를 비교하고, "
    "상자 밖에 나타나는 영화가 해당 장르에서 관객수가 특히 높은 영화인지 살펴볼 수 있습니다."
)

# ==================================================
# 여섯 번째 그래프
# ==================================================

st.markdown("---")

st.subheader("🫧 첫 주 관객을 크기로 나타낸 버블 그래프")

# 버블 그래프에 사용할 데이터
bubble_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "movieNm",
        "genre_first"
    ]
).copy()

# 숫자형으로 변환
bubble_df["first_scrn"] = pd.to_numeric(
    bubble_df["first_scrn"],
    errors="coerce"
)

bubble_df["total_audi"] = pd.to_numeric(
    bubble_df["total_audi"],
    errors="coerce"
)

bubble_df["first_week_audi"] = pd.to_numeric(
    bubble_df["first_week_audi"],
    errors="coerce"
)

bubble_df = bubble_df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi"
    ]
)

# 음수 값 제거
bubble_df = bubble_df[
    (bubble_df["first_scrn"] >= 0) &
    (bubble_df["total_audi"] >= 0) &
    (bubble_df["first_week_audi"] >= 0)
]

# 버블 그래프
fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre_first",
    hover_name="movieNm",
    hover_data={
        "first_scrn": ":,",
        "total_audi": ":,",
        "first_week_audi": ":,",
        "genre_first": True
    },
    size_max=45,
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "first_week_audi": "첫 주 관객",
        "genre_first": "장르"
    },
    title="개봉일 스크린수·총 관객수·첫 주 관객의 관계"
)

fig6.update_traces(
    marker=dict(
        opacity=0.7
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객수: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    height=650,
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객수",
    legend_title="장르"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# 그래프 설명 구역
st.markdown("---")

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "개봉일 스크린수와 총 관객수의 관계를 살펴보면서, "
    "버블의 크기로 첫 주 관객 규모까지 함께 비교할 수 있습니다."
)

# ── 그래프 7. 국가에서 장르로 (선버스트) ──
st.markdown("---")

st.subheader("🌞 국가에서 장르로 (선버스트)")

# 여러 국가가 |로 연결되어 있으면 첫 번째 국가만 사용
df["대표국가"] = (
    df["nation"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 대표 국가 + 첫 번째 장르별 영화 편수
counted = (
    df.groupby(
        ["대표국가", "genre_first"],
        as_index=False
    )
    .agg(편수=("movieNm", "count"))
)

# 선버스트 그래프
fig7 = px.sunburst(
    counted,
    path=["대표국가", "genre_first"],
    values="편수",
    title="국가에서 장르로"
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    height=650
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

# 그래프 설명 구역
st.markdown("---")

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "국가별로 어떤 장르의 영화가 많이 만들어졌는지와 장르별 영화 편수의 차이를 한눈에 비교할 수 있습니다."
)
