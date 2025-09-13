import streamlit as st

# 🎨 페이지 기본 설정
st.set_page_config(page_title="MBTI Study Buddy", page_icon="📚", layout="centered")

# 🌟 제목과 설명
st.title("📖 MBTI별 공부 방법 추천기 ✨")
st.markdown("공부가 잘 안 될 땐? 👉 MBTI에 맞는 공부법을 찾아보세요! 💡")

# MBTI 리스트
mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# MBTI별 공부법 추천 딕셔너리
study_tips = {
    "ISTJ": "✅ 계획표를 꼼꼼히 세우고, 체크리스트로 하나씩 완료하세요!", 
    "ISFJ": "🤝 친구와 함께 공부하면 동기부여가 UP!", 
    "INFJ": "🌌 조용한 공간에서 목표를 시각화하며 공부하세요!", 
    "INTJ": "📊 장기 플랜을 세우고 체계적으로 학습하면 효과적!", 
    "ISTP": "🛠️ 직접 문제를 풀어보고 손으로 정리하는 방식이 좋아요!", 
    "ISFP": "🎶 음악과 함께 몰입할 수 있는 분위기를 만들어보세요!", 
    "INFP": "💭 상상을 곁들여 창의적으로 공부하세요!", 
    "INTP": "🔍 원리를 깊게 파고드는 공부법이 잘 맞습니다!", 
    "ESTP": "⚡ 짧고 집중적인 스터디 세션으로 효율을 높여보세요!", 
    "ESFP": "🎉 게임처럼 즐길 수 있는 방식으로 공부하세요!", 
    "ENFP": "🌈 다양한 자료를 접하고 아이디어 노트에 정리해보세요!", 
    "ENTP": "🗣️ 토론과 설명을 통해 이해도를 높이세요!", 
    "ESTJ": "📅 시간 관리 철저! 계획대로 차근차근 밀고 나가세요!", 
    "ESFJ": "👯‍♀️ 스터디 그룹과 함께 공부하면 효과 만점!", 
    "ENFJ": "💡 다른 사람을 가르치듯 설명하면서 공부하세요!", 
    "ENTJ": "🚀 목표를 정하고 속도감 있게 추진하는 학습이 잘 맞습니다!"
}

# 사용자 선택
choice = st.selectbox("👉 나의 MBTI는?", mbti_types)

# 추천 결과 표시
if choice:
    st.subheader(f"✨ {choice} 타입에게 딱 맞는 공부법은... ✨")
    st.success(study_tips[choice])

    # 🎉 재미있는 효과
    if choice in ["ENFP", "ESFP", "ENTP"]:
        st.balloons()  # 활발한 유형은 풍선 효과!
    elif choice in ["INFJ", "INFP", "INTP"]:
        st.snow()  # 몽환적인 유형은 눈 효과!
    else:
        st.progress(100)  # 계획적인 유형은 진척도 막대기로 마무리!

# 푸터
st.markdown("---")
st.markdown("Made with ❤️ and Streamlit ✨")
