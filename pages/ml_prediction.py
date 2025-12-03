import streamlit as st
import pickle
import numpy as np
from pathlib import Path

st.header("🌸 붓꽃 품종 예측")

# 모델 경로 설정
SCRIPT_DIR = Path(__file__).parent.parent
MODEL_PATH = SCRIPT_DIR / "model" / "iris_model.pkl"


# 모델 로드 (캐싱)
@st.cache_resource
def load_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


model = load_model()

if model is None:
    st.error("모델 파일이 없습니다! 먼저 `python train_model.py`를 실행하세요.")
else:
    # ML 예측 UI
    @st.fragment
    def ml_prediction():
        st.success("모델 로드 완료!")

        col1, col2 = st.columns(2)
        with col1:
            sepal_length = st.slider("꽃받침 길이 (cm)", 4.0, 8.0, 5.0)
            sepal_width = st.slider("꽃받침 너비 (cm)", 2.0, 4.5, 3.0)
        with col2:
            petal_length = st.slider("꽃잎 길이 (cm)", 1.0, 7.0, 4.0)
            petal_width = st.slider("꽃잎 너비 (cm)", 0.1, 2.5, 1.0)

        st.divider()

        # 예측 (스피너로 진행 표시)
        with st.spinner("🤖 품종 예측 중..."):
            input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
            prediction = model.predict(input_data)[0]
            proba = model.predict_proba(input_data)[0]

        species = ["Setosa", "Versicolor", "Virginica"]

        st.subheader("예측 결과")
        st.success(f"예측 품종: **{species[prediction]}**")

        # 확률 표시
        st.write("품종별 확률:")
        for name, prob in zip(species, proba):
            st.progress(prob, text=f"{name}: {prob:.1%}")

    ml_prediction()
