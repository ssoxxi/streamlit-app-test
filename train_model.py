"""
모델 훈련 스크립트
이 파일을 먼저 실행하여 모델을 저장한 후, app.py를 실행하세요.

실행: python train_model.py
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pickle
from pathlib import Path

# 현재 스크립트 위치 기준으로 model 폴더 생성
SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"
MODEL_DIR.mkdir(exist_ok=True)

# 데이터 로드 및 훈련
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 정확도 출력
accuracy = model.score(X_test, y_test)
print(f"모델 정확도: {accuracy:.2%}")

# 모델 저장
model_path = MODEL_DIR / "iris_model.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)
print(f"모델 저장 완료! ({model_path})")
