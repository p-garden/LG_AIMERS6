# -*- coding: utf-8 -*-
"""현재 1등.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eyYRn0zSpjMproEnryFPHkj1-VEkgXYS
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install autogluon

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/AIMERS/

import warnings
warnings.simplefilter("ignore", category=FutureWarning)

import ray

# Ray 초기화 시 CPU 수를 최대한 활용하도록 설정
ray.shutdown()  # 기존 세션 종료
ray.init(num_cpus=32)  # 현재 Colab에서 사용 가능한 최대 CPU로 설정

print(f"사용 가능한 CPU 개수: {ray.available_resources().get('CPU', 0)}")

import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

#########################################
#########################################
def preprocess_data(df):

    # 제거할 컬럼
    drop_columns = [
        '불임 원인 - 여성 요인',
        '불임 원인 - 자궁경부 문제', '미세주입 후 저장된 배아 수', '불임 원인 - 정자 면역학적 요인',
        '불임 원인 - 정자 운동성', '시술 유형', '난자 해동 경과일', 'DI 출산 횟수', '저장된 신선 난자 수',
        '정자 출처', '임신 시도 또는 마지막 임신 경과 연수',
        '부부 부 불임 원인', '여성 부 불임 원인', '불임 원인 - 정자 형태', '대리모 여부', '불임 원인 - 정자 농도',
        'DI 임신 횟수', '기증 배아 사용 여부', '착상 전 유전 진단 사용 여부', '미세주입 배아 이식 수',
        '부부 주 불임 원인', '기증자 정자와 혼합된 난자 수', '배아 해동 경과일', 'PGD 시술 여부', '파트너 정자와 혼합된 난자 수',
        '혼합된 난자 수', '불임 원인 - 자궁경부 문제'
    ]

    df = df.drop(columns=[col for col in drop_columns if col in df.columns])

    # ✅ 피처 엔지니어링 적용
    df["배아 수 제곱"] = df["이식된 배아 수"] ** 2



    # ✅ 연령대를 중앙값으로 변환하여 숫자로 변환
    age_mapping = {
        "만18-34세": 26,
        "만35-37세": 36,
        "만38-39세": 38.5,
        "만40-42세": 41,
        "만43-44세": 43.5,
        "만45-50세": 47.5,
        "알 수 없음": -1  # "알 수 없음"을 특별한 값으로 처리
    }

    # ✅ 매핑 적용
    df["시술 당시 나이 숫자"] = df["시술 당시 나이"].map(age_mapping)

    # 배아 개수 대비 저장된 배아 수 비율 (배아 보존율)
    df["배아 보존율"] = df["저장된 배아 수"] / (df["총 생성 배아 수"] + 1)  # 0으로 나누는 것 방지

    # ✅ 나이와 배아 수의 비율 변수 생성
    df["배아 수 대비 나이"] = df["시술 당시 나이 숫자"] / (df["이식된 배아 수"] + 1)

    # ✅ 추가 비율 Feature 생성
    df["배아 이식 경과일 대비 나이"] = df["배아 이식 경과일"] / (df["시술 당시 나이 숫자"] + 1)




    df["1~2개 이식 여부"] = (df["이식된 배아 수"].between(1, 2)).astype(int)

    df["나이 26~36 여부"] = ((df["시술 당시 나이 숫자"] >= 26) &
                      (df["시술 당시 나이 숫자"] <= 36)).astype(int)

    # 1️⃣ 이식된 배아 수 × 시술 당시 나이 숫자
    df["이식된 배아 수 × 시술 당시 나이"] = df["이식된 배아 수"] * df["시술 당시 나이 숫자"]

    # 2️⃣ 배아 이식 경과일 대비 나이 × 배아 수 대비 나이
    df["배아 이식 경과일 대비 나이 × 배아 수 대비 나이"] = df["배아 이식 경과일 대비 나이"] * df["배아 수 대비 나이"]

    # 3️⃣ 배아 수 대비 나이 / 총 생성 배아 수
    df["배아 수 대비 나이 / 총 생성 배아 수"] = df["배아 수 대비 나이"] / (df["총 생성 배아 수"] + 1)

    # 4️⃣ 이식된 배아 수 × 배아 이식 경과일 대비 나이
    df["이식된 배아 수 × 배아 이식 경과일 대비 나이"] = df["이식된 배아 수"] * df["배아 이식 경과일 대비 나이"]

    # 5️⃣ 시술 당시 나이 숫자 / 총 생성 배아 수
    df["시술 당시 나이 숫자 / 총 생성 배아 수"] = df["시술 당시 나이 숫자"] / (df["총 생성 배아 수"] + 1)






    return df

import pandas as pd
from autogluon.tabular import TabularPredictor

# ✅ 데이터 로드
train = pd.read_csv("data/train.csv")
test = pd.read_csv("data/test.csv")

train = preprocess_data(train)
test = preprocess_data(test)

# ✅ ID 제거
train = train.drop(columns=["ID"])
test_id = test["ID"]
test= test.drop(columns=["ID"])

# ✅ 모델 저장 경로
save_path = "new_start5"

hyperparameters = {
    "GBM": {},
    "CAT": {},
    "XGB": {},
    "RF": {},
    "FASTAI": {},
    "XT": {},
    "NN_TORCH": {}
}

from autogluon.tabular import TabularPredictor

# 📌 2️⃣ 모델 학습 설정
predictor = TabularPredictor(label="임신 성공 여부", eval_metric="roc_auc", path=save_path)

predictor.fit(
    train_data=train,
    presets="best_quality",
    time_limit=3600*12,  # 학습 제한 시간 (초)
    num_bag_folds=8,  # Bagging 적용
    num_stack_levels=0,  # Stacking 미사용
    dynamic_stacking=False,
    save_space=True,
    hyperparameters = hyperparameters,
    hyperparameter_tune_kwargs = {
        "num_trials": 20,  # 🚀 각 모델당 25번의 랜덤 탐색
        "scheduler": "local",
        "searcher": "random"
    }
)

# 📌 3️⃣ 예측 수행
pred = predictor.predict_proba(test)
submission = pd.DataFrame({"ID": test_id, "probability": pred[1]})

# 결과 병합 및 저장
submission.to_csv("new_start5/Submission_new8_20_12time.csv", index=False)

print("Submission file created: Submission19.csv")

# 리더보드 출력
predictor.leaderboard(silent=False)

# 리더보드 출력
predictor.leaderboard(silent=False)

importance = predictor.feature_importance(train)
print(importance)

importance.head(40)

importance.tail(33)