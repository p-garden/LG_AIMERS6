# -*- coding: utf-8 -*-
"""preprocess_mljar.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pCuKv7MsC76AW14XhcG5NQu0MSE1wqIK
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/AIMERS/

pip install mljar-supervised

from supervised.automl import AutoML
import pandas as pd
from sklearn.model_selection import train_test_split
import category_encoders as ce
import joblib
from sklearn.metrics import roc_auc_score
# 📌 데이터 로드
train = pd.read_csv("data/train.csv")
test = pd.read_csv("data/test.csv")

# 🔹 ID 컬럼 저장
test_id = test["ID"]

# 🔹 불필요한 열 제거 (ID는 학습에 필요 없음)
train = train.drop(columns=["ID"])
test = test.drop(columns=["ID"])

"""## 직접 전처리
AutoML은 일괄적으로 칼럼들에대해 전처리를 진행하므로 칼럼 특성에 맞춰 직접 전처리 진행  
결측치 처리, 범주형 변수 처리, 표준화 로 나누어 진행

### 결측치 관련 처리
"""

for df in [train, test]:

    # 2️⃣ 본인 난자 사용 여부 (난자 채취 경과일이 존재하면 1)
    df["본인 난자 사용 여부"] = df["난자 채취 경과일"].notnull().astype(int)

    # 3️⃣ 동결 난자 사용 여부 (해동 난자 수가 1개 이상이면 1)
    df["동결 난자 사용 여부"] = (df["해동 난자 수"] >= 1).astype(int)

    # 4️⃣ 기증 난자 사용 여부 (난자 출처가 '기증 제공'이면 1)
    df["기증 난자 사용 여부"] = (df["난자 출처"] == "기증 제공").astype(int)

    # 5️⃣ 동결 배아 사용 여부 (동결 배아 사용 여부가 1이면 1)
    df["동결 배아 사용 여부"] = (df["동결 배아 사용 여부"] == 1).astype(int)

    # 6️⃣ 기증 배아 사용 여부 (기증 배아 사용 여부가 1이면 1)
    df["기증 배아 사용 여부"] = (df["기증 배아 사용 여부"] == 1).astype(int)

for df in [train, test]:
    df["유전 검사 여부"] = '0'  # 기본값 0 (IVF가 아닌 경우)

    # IVF 시술 여부 필터
    ivf_mask = df["시술 유형"] == "IVF"

    # PGS 또는 PGD 시술 여부 확인
    genetic_test_mask = df["PGS 시술 여부"].notnull() | df["PGD 시술 여부"].notnull()

    # IVF이면서 PGS 또는 PGD 중 하나라도 있으면 1
    df.loc[ivf_mask & genetic_test_mask, "유전 검사 여부"] = '1'

    # IVF이면서 둘 다 없는 경우 'Unknown' 처리
    df.loc[ivf_mask & ~genetic_test_mask, "유전 검사 여부"] = "Unknown"

for df in [train, test]:
    df["과거 임신 성공 여부"] = df["총 임신 횟수"].map({
        "0회": 0,  # 임신 경험 없음
        "1회": 1, "2회": 1, "3회": 1, "4회": 1, "5회": 1, "6회 이상": 1  # 임신 경험 있음
    }).fillna(0).astype(int)  # 결측값은 0으로 처리

for df in [train, test]:
    df["배아 이식 경과일"] = df["배아 이식 경과일"].fillna(3)

drop_cols = [
    "난자 해동 경과일", "PGS 시술 여부", "PGD 시술 여부", "착상 전 유전 검사 사용 여부",
    "임신 시도 또는 마지막 임신 경과 연수", "배아 해동 경과일", "난자 채취 경과일", "난자 혼합 경과일"
]

train = train.drop(columns=drop_cols)
test = test.drop(columns=drop_cols)
print(train.columns)
print(test.columns)

"""### 범주형 변수 관련 처리"""

# 범주형 변수 확인
categorical_cols_train = train.select_dtypes(include=["object"]).columns.tolist()
categorical_cols_train

import category_encoders as ce
import joblib

target_encoder = ce.TargetEncoder(cols=["시술 당시 나이"])
train["시술 당시 나이"] = target_encoder.fit_transform(train["시술 당시 나이"], train["임신 성공 여부"])
test["시술 당시 나이"] = target_encoder.transform(test["시술 당시 나이"])

from sklearn.preprocessing import LabelEncoder

# Label Encoding 적용
label_encoder = LabelEncoder()
train["시술 유형"] = label_encoder.fit_transform(train["시술 유형"])
test["시술 유형"] = label_encoder.transform(test["시술 유형"])

train["특정 시술 유형"].value_counts()

# 타깃 인코딩 적용할 범주형 변수 선택
categorical_cols = ["특정 시술 유형"]

# 타깃 인코딩 수행
target_encoder = ce.TargetEncoder(cols=categorical_cols, smoothing=0.3)
train["특정 시술 유형"] = target_encoder.fit_transform(train["특정 시술 유형"],  train["임신 성공 여부"])
test["특정 시술 유형"] = target_encoder.transform(test["특정 시술 유형"])



train['배란 유도 유형'].value_counts()

train["배란 유도 여부"] = train["배란 유도 유형"].apply(lambda x: 1 if x in ["세트로타이드 (억제제)", "생식선 자극 호르몬"] else 0)
test["배란 유도 여부"] = test["배란 유도 유형"].apply(lambda x: 1 if x in ["세트로타이드 (억제제)", "생식선 자극 호르몬"] else 0)

# 원래 변수 제거
train = train.drop(columns=["배란 유도 유형"])
test = test.drop(columns=["배란 유도 유형"])

train["배아 생성 주요 이유"].value_counts()

import category_encoders as ce

# 타깃 인코딩 적용
target_encoder = ce.TargetEncoder(cols=["배아 생성 주요 이유"], smoothing=0.3)
train["배아 생성 주요 이유"] = target_encoder.fit_transform(train["배아 생성 주요 이유"],  train["임신 성공 여부"])
test["배아 생성 주요 이유"] = target_encoder.transform(test["배아 생성 주요 이유"])

# "횟수" 컬럼들 리스트
count_cols = [
    "총 시술 횟수", "클리닉 내 총 시술 횟수", "IVF 시술 횟수", "DI 시술 횟수",
    "총 임신 횟수", "IVF 임신 횟수", "DI 임신 횟수",
    "총 출산 횟수", "IVF 출산 횟수", "DI 출산 횟수"
]

# "횟수" 데이터를 숫자로 변환하는 함수
def convert_count(value):
    if isinstance(value, str):  # 문자열이면 처리
        if "이상" in value:  # "6회 이상" 같은 경우
            return int(value.split("회")[0]) + 1  # 6회 이상 → 7로 변환
        return int(value.replace("회", ""))  # '3회' → 3으로 변환
    return value  # 이미 숫자인 경우 그대로 반환

# 변환 적용
for col in count_cols:
    train[col] = train[col].apply(convert_count)
    test[col] = test[col].apply(convert_count)

print("✅ '횟수' 칼럼 숫자 변환 완료!")

train["정자 출처"].value_counts()

# 원-핫 인코딩 적용
train = pd.get_dummies(train, columns=["난자 출처", "정자 출처"], dtype=int)
test = pd.get_dummies(test, columns=["난자 출처", "정자 출처"], dtype=int)

print("✅ '난자 출처', '정자 출처' 원-핫 인코딩 완료!")

train["정자 기증자 나이"].value_counts()

import category_encoders as ce

# 타깃 인코딩 수행
target_encoder = ce.TargetEncoder(cols=["난자 기증자 나이", "정자 기증자 나이"], smoothing=0.3)
train[["난자 기증자 나이", "정자 기증자 나이"]] = target_encoder.fit_transform(train[["난자 기증자 나이", "정자 기증자 나이"]], train["임신 성공 여부"])
test[["난자 기증자 나이", "정자 기증자 나이"]] = target_encoder.transform(test[["난자 기증자 나이", "정자 기증자 나이"]])

print("✅ '난자 기증자 나이', '정자 기증자 나이' 타깃 인코딩 완료!")

train["유전 검사 여부"].value_counts()

# '유전 검사 여부' 값별 임신 성공 여부 평균 계산
probabilities = train.groupby("유전 검사 여부")["임신 성공 여부"].mean()

# 결과 출력
probabilities

# 유전 검사 여부 칼럼을 타깃 인코딩 적용
target_encoder = ce.TargetEncoder(cols=['유전 검사 여부'], smoothing=0.3)

# 학습 데이터에 대해 타깃 인코딩 적용
train['유전 검사 여부'] = target_encoder.fit_transform(train['유전 검사 여부'], train['임신 성공 여부'])

# 테스트 데이터에도 동일한 변환 적용
test['유전 검사 여부'] = target_encoder.transform(test['유전 검사 여부'])

drop_cols = ['시술 시기 코드']
train = train.drop(columns=drop_cols)
test = test.drop(columns=drop_cols)

# 범주형 변수 확인
categorical_cols_test = test.select_dtypes(include=["object"]).columns.tolist()
categorical_cols_test

# 남성 불임 원인의 값 분포
print(train["남성 주 불임 원인"].value_counts())

# 남성 불임 원인 값별 임신 성공률 확인
success_rate = train.groupby("남성 주 불임 원인")["임신 성공 여부"].mean()
print(success_rate)

"""### 표준화"""

# 숫자형 변수 선택
numeric_cols = train.select_dtypes(include=['int64', 'float64']).columns

# 각 숫자형 속성들의 최소값, 최대값 범위 확인
range_train = train[numeric_cols].agg(['min', 'max']).T
range_train.columns = ['Min', 'Max']

# 모든 행을 출력할 수 있도록 설정
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# 최소값과 최대값 출력
print(range_train)

# 1을 초과하는 최대값을 가진 열들 찾기
cols_to_scale = range_train[range_train["Max"] > 1].index.tolist()
print(f"✅ 표준화 적용 대상 칼럼: {cols_to_scale}")

from sklearn.preprocessing import StandardScaler

# 표준화 적용
scaler = StandardScaler()
train[cols_to_scale] = scaler.fit_transform(train[cols_to_scale])
test[cols_to_scale] = scaler.transform(test[cols_to_scale])

print("✅ 표준화 적용 완료!")

train.describe()

test.info()



"""## AutoML 적용"""

# 🔹 특징(X)와 타겟(y) 분리
X_train = train.drop(columns=["임신 성공 여부"])
y_train = train["임신 성공 여부"]
X_test = test.copy()

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42, stratify=y_train)

automl = AutoML(
    mode="Compete",
    total_time_limit=3600,
    eval_metric="auc",  # 평가 기준을 ROC-AUC로 설정
    golden_features=True,  # 중요한 피처 생성
    kmeans_features=True,  # K-means 기반 피처 생성
    mix_encoding=True,  # 다양한 인코딩 적용
    algorithms=["CatBoost", "LightGBM", "Xgboost"],  # 성능이 낮은 모델 제외

)

automl.fit(X_train, y_train)

# ✅ 검증 (Validation Set으로 성능 확인)
val_preds = automl.predict_proba(X_val)[:, 1]  # 확률값 예측
val_auc = roc_auc_score(y_val, val_preds)  # ROC-AUC 계산

print(f"\n🎯 검증 데이터 ROC-AUC: {val_auc:.4f}")

# 📌 예측 수행
preds = automl.predict_proba(X_test)[:, 1]

# 📌 결과 저장
submission = pd.DataFrame({"ID": test_id, "probability": preds})
submission.to_csv("submission_mljar.csv", index=False, encoding="utf-8-sig")

print("\n✅ [결과 저장 완료] 파일: submission_mljar.csv")

automl.get_leaderboard()

leaderboard = automl.get_leaderboard()
leaderboard

import json
import pandas as pd
import matplotlib.pyplot as plt

# 🔹 파일 경로 수정 (AutoML_3 폴더 내 파일 로드)
golden_features_path = "AutoML_3/golden_features.json"

# 🔹 피처 중요도 로드
with open(golden_features_path, "r", encoding="utf-8") as f:
    golden_features = json.load(f)

# 🔹 피처 중요도 데이터프레임 변환
# 데이터프레임 변환
feature_importance = pd.DataFrame(golden_features["new_features"])
feature_importance = feature_importance.sort_values(by="score", ascending=False)

# 모든 피처 중요도 출력
pd.set_option('display.max_rows', None)  # 모든 행 출력
print(feature_importance)

