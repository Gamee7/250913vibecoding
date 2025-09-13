import streamlit as st
import pandas as pd
import altair as alt
import os

# 제목
st.title("🌍 MBTI 유형별 분포 분석")

# 데이터 불러오기
@st.cache_data
def load_data():
    file_path = "countriesMBTI_16types.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            st.stop()
    return df

df = load_data()

# MBTI 유형 리스트 추출
mbti_types = [col for col in df.columns if col != "Country"]

# 사용자 선택
selected_type = st.selectbox("분석할 MBTI 유형을 선택하세요:", mbti_types)

# 선택된 유형 TOP 10 국가 추출
top10 = df[["Country", selected_type]].sort_values(by=selected_type, ascending=False).head(10)

# Altair 그래프 그리기
chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X(selected_type, title="비율"),
        y=alt.Y("Country", sort="-x", title="국가"),
        tooltip=["Country", selected_type],
        color=alt.Color("Country", legend=None)
    )
    .interactive()
)

st.subheader(f"{selected_type} 유형 비율이 높은 국가 TOP 10")
st.altair_chart(chart, use_container_width=True)
