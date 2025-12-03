import streamlit as st

st.title("🤖 ML & AI 통합 앱")

st.markdown("""
이 앱은 **머신러닝 예측**, **Gemini AI 챗봇**, **음악 DB 분석**을 제공합니다.

---

### 📌 기능 소개

| 기능 | 설명 |
|------|------|
| 🌸 **붓꽃 품종 예측** | 꽃받침/꽃잎 크기로 품종 분류 (RandomForest) |
| 💬 **Gemini 챗봇** | Google Gemini API 기반 대화형 AI |
| 🎵 **음악 DB 분석** | Chinook DB 기반 음악 데이터 분석 |

---

### 🚀 시작하기

왼쪽 사이드바에서 원하는 기능을 선택하세요!
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🌸 **붓꽃 품종 예측**\n\n슬라이더로 꽃의 특성을 입력하면 AI가 품종을 예측합니다.")

with col2:
    st.info("💬 **Gemini 챗봇**\n\nGoogle의 최신 AI 모델과 대화해보세요.")

with col3:
    st.info("🎵 **음악 DB 분석**\n\n아티스트, 장르, 매출 등 음악 데이터를 분석합니다.")
