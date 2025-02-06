# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # 1. 결측치 분석

# +
import pandas as pd

# 데이터 파일 경로
file_path = "data/train.csv"

# 데이터 로드
df = pd.read_csv(file_path)

# 데이터 기본 정보 확인
df_info = df.info()
df_head = df.head()

df_info, df_head


# +
# 한글 폰트 설정 (Matplotlib에서 한글 깨짐 방지)
import matplotlib.pyplot as plt
import matplotlib

# 한글 폰트 설정 (Windows 환경)
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows에서는 'Malgun Gothic' 사용

# 마이너스 부호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# 현재 설정된 폰트 확인
matplotlib.rcParams['font.family']


# +
import pandas as pd

# 결측치 비율 계산
missing_values = df.isnull().sum() / len(df) * 100

# 결측치가 있는 컬럼만 필터링하여 내림차순 정렬
missing_values = missing_values[missing_values > 0].sort_values(ascending=False)

# 데이터프레임으로 변환하여 보기 좋게 출력
missing_df = pd.DataFrame({'Column': missing_values.index, 'Missing Percentage': missing_values.values})

# 결측치 분석 결과 출력
print(missing_df)


# + [markdown] jp-MarkdownHeadingCollapsed=true
# ##### 난자 배아 해동 경과일 칼럼 분석
# -



# +
# 특정 시술 유형이 'FER'인 경우의 난자 해동 경과일 결측 여부 확인
fer_subset = df[df['특정 시술 유형'] == 'FER']

# 난자 해동 경과일이 결측치가 아닌 경우의 비율 계산
fer_non_null_ratio = fer_subset['난자 해동 경과일'].notnull().mean() * 100

# 전체 데이터에서 특정 시술 유형이 'FER'인 경우의 비율 확인
fer_ratio_in_data = len(fer_subset) / len(df) * 100

# 출력 결과 확인
fer_non_null_ratio, fer_ratio_in_data


# +
# 난자 해동 경과일이 non-null인 행만 필터링
non_null_egg_thawing = df[df['난자 해동 경과일'].notnull()]

# 해당 데이터의 기본 정보 확인
non_null_egg_thawing_info = non_null_egg_thawing.info()

# 상위 몇 개 행 출력
non_null_egg_thawing_head = non_null_egg_thawing.head()

non_null_egg_thawing_info, non_null_egg_thawing_head


# +
import matplotlib.pyplot as plt

# 1. 특정 시술 유형과 난자 해동 경과일 관계
procedure_counts = non_null_egg_thawing['특정 시술 유형'].value_counts()

plt.figure(figsize=(12, 5))
procedure_counts.plot(kind='bar', title="특정 시술 유형 분포 (난자 해동 경과일이 있는 경우)")
plt.xlabel("특정 시술 유형")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()

# 2. 난자 해동 경과일과 배아 해동 경과일 관계
plt.figure(figsize=(8, 5))
plt.scatter(non_null_egg_thawing['난자 해동 경과일'], non_null_egg_thawing['배아 해동 경과일'], alpha=0.5)
plt.title("난자 해동 경과일 vs 배아 해동 경과일")
plt.xlabel("난자 해동 경과일")
plt.ylabel("배아 해동 경과일")
plt.show()

# 3. 난자 해동 경과일의 분포
plt.figure(figsize=(8, 5))
non_null_egg_thawing['난자 해동 경과일'].hist(bins=20, edgecolor='black')
plt.title("난자 해동 경과일 분포")
plt.xlabel("난자 해동 경과일")
plt.ylabel("Count")
plt.show()

# -

# non-null값의 대부분이 0  
# 극 소수의 값만 1  
# -> 난자 해동 하루 안걸림  
# 열 삭제 or null값 0으로 대체(난자 얼린 경우만)

# +
# 해동 난자 수가 1 이상인데 난자 해동 경과일이 null인 경우 필터링
egg_thawed_but_null_days = df[(df['해동 난자 수'] >= 1) & (df['난자 해동 경과일'].isnull())]

# 해당 경우의 개수 확인
num_cases = len(egg_thawed_but_null_days)

# 상위 몇 개 샘플 출력
egg_thawed_but_null_days_sample = egg_thawed_but_null_days.head()

num_cases, egg_thawed_but_null_days_sample

# -





# +
# 해동 난자 수가 1 이상인데 난자 해동 경과일이 null인 경우 필터링
egg_thawed_but_null_days = df[(df['해동 난자 수'] >= 1) & (df['난자 해동 경과일'].notnull())]

# 해당 경우의 개수 확인
num_cases = len(egg_thawed_but_null_days)

num_cases, egg_thawed_but_null_days['난자 해동 경과일'].describe()


# +
# 4가지 경우에 대한 필터링
case_1 = df[(df['해동 난자 수'] >= 1) & (df['난자 해동 경과일'].isnull())]
case_2 = df[(df['해동 난자 수'] >=1) & (df['난자 해동 경과일'].notnull())]
case_3 = df[(df['해동 난자 수'] == 0) & (df['난자 해동 경과일'].isnull())]
case_4 = df[(df['해동 난자 수'] == 0) & (df['난자 해동 경과일'].notnull())]

# 각 경우의 개수 확인
case_counts = {
    "해동 난자 수 >1 & 난자 해동 경과일 NULL": len(case_1),
    "해동 난자 수 >1 & 난자 해동 경과일 non-NULL": len(case_2),
    "해동 난자 수 =0 & 난자 해동 경과일 NULL": len(case_3),
    "해동 난자 수 =0 & 난자 해동 경과일 non-NULL": len(case_4)
}

# 각 경우의 통계 정보 확인
case_stats = {
    "해동 난자 수 >1 & 난자 해동 경과일 NULL": case_1['해동 난자 수'].describe(),
    "해동 난자 수 >1 & 난자 해동 경과일 non-NULL": case_2['해동 난자 수'].describe(),
    "해동 난자 수 =0 & 난자 해동 경과일 NULL": case_3['해동 난자 수'].describe(),
    "해동 난자 수 =0 & 난자 해동 경과일 non-NULL": case_4['해동 난자 수'].describe()
}

# 결과 출력
case_counts, case_stats

# -

case_4

# 난자 해동했으면 0 / 난자 해동 안했으면'Nan'으로 대체

# +
import matplotlib.pyplot as plt

# 난자 해동 경과일이 Non-NULL인 데이터 필터링
egg_thawing_non_null = df[df['난자 해동 경과일'].notnull()]

# 해동된 난자 수가 0인 경우의 비중 계산
thawed_egg_zero_ratio = (egg_thawing_non_null['해동 난자 수'] == 0).sum()


# 2. 해동된 난자 수 분포 시각화
plt.figure(figsize=(8, 5))
egg_thawing_non_null['해동 난자 수'].hist(bins=30, edgecolor='black')
plt.title("해동된 난자 수 분포")
plt.xlabel("해동된 난자 수")
plt.ylabel("빈도")
plt.show()

# 해동된 난자 수가 0인 경우의 비중 출력
print(f"해동된 난자 수가 0인 경우 수: {thawed_egg_zero_ratio:.2f}")


# + [markdown] jp-MarkdownHeadingCollapsed=true
# ##### PGS 시술 여부 & PGD 시술 여부 칼럼 분석

# +
# IVF 시술 여부에 따른 그룹 나누기
ivf_group = df['시술 유형'] == 'IVF'

# PGS/PGD 시술 여부가 NULL/Non-NULL인지 구분
pgs_null = df['PGS 시술 여부'].isnull()
pgd_null = df['PGD 시술 여부'].isnull()

# 경우의 수 계산
case_counts = {
    "IVF & PGS NULL & PGD NULL": len(df[ivf_group & pgs_null & pgd_null]),
    "IVF & PGS NULL & PGD Non-NULL": len(df[ivf_group & pgs_null & ~pgd_null]),
    "IVF & PGS Non-NULL & PGD NULL": len(df[ivf_group & ~pgs_null & pgd_null]),
    "IVF & PGS Non-NULL & PGD Non-NULL": len(df[ivf_group & ~pgs_null & ~pgd_null]),
    "Non-IVF & PGS NULL & PGD NULL": len(df[~ivf_group & pgs_null & pgd_null]),
    "Non-IVF & PGS NULL & PGD Non-NULL": len(df[~ivf_group & pgs_null & ~pgd_null]),
    "Non-IVF & PGS Non-NULL & PGD NULL": len(df[~ivf_group & ~pgs_null & pgd_null]),
    "Non-IVF & PGS Non-NULL & PGD Non-NULL": len(df[~ivf_group & ~pgs_null & ~pgd_null]),
}

# 결과 출력
case_counts


# +
# PGS 시술 여부와 PGD 시술 여부가 모두 1인 경우 필터링
pgs_pgd_both_1 = df[(df['PGS 시술 여부'] == 1) & (df['PGD 시술 여부'] == 1)]

# 해당 경우의 개수 확인
num_pgs_pgd_both_1 = len(pgs_pgd_both_1)

# 상위 몇 개 샘플 출력
pgs_pgd_both_1_sample = pgs_pgd_both_1.head()

num_pgs_pgd_both_1, pgs_pgd_both_1_sample
# 하나도 없음

# +
# IVF 시술을 받은 경우 중 PGS 시술 여부가 Non-NULL인 데이터에서 PGS 시술 여부 분포
pgs_non_null_distribution = df[df['시술 유형'] == 'IVF']['PGS 시술 여부'].dropna().value_counts(normalize=True) * 100

# IVF 시술을 받은 경우 중 PGD 시술 여부가 Non-NULL인 데이터에서 PGD 시술 여부 분포
pgd_non_null_distribution = df[df['시술 유형'] == 'IVF']['PGD 시술 여부'].dropna().value_counts(normalize=True) * 100

# 결과 출력
pgs_non_null_distribution, pgd_non_null_distribution
# nonnull값은 항상 시술한 경우 

# +
# IVF 시술을 받은 경우 필터링
ivf_data = df[df['시술 유형'] == 'IVF']

# 연령대별 PGS, PGD 시술 여부가 Non-NULL인 경우의 확률 계산
age_pgs_pgd_stats = ivf_data.groupby('시술 당시 나이').apply(
    lambda x: pd.Series({
        'PGS 검사 확률 (%)': (x['PGS 시술 여부'].notnull().mean()) * 100,
        'PGD 검사 확률 (%)': (x['PGD 시술 여부'].notnull().mean()) * 100
    })
).reset_index()

# 결과 출력
age_pgs_pgd_stats
# -

# - `IVF` 시술을 받은 경우에만 `PGS` 또는 `PGD` 시술 여부가 기록됨.
# - 하지만 `PGS`와 `PGD`가 동시에 적용된 사례는 없음.
#     
#     → 둘 중 하나가 non-null인 경우는 해결(toggle)
#     
# - Non-IVF 시술을 받은 경우 `PGS`와 `PGD`는 아예 기록되지 않음.
#     
#     → Non-IVF인 경우는 해결(둘다 0)
#     
# - `PGS` `PGD` 시술여부는 항상 1로만 기록 → 0인경우는 NULL(?)
# - IVF 시술을 할 때 항상 PGS 또는 PGD 검사를 시행하는 것은 아님 / 필요한 경우에만 시행
#     
#     IVF 환자 중 PGS 검사 확률: 20~40%(나이에 따라 다름)
#     
#     PGD 검사 확률: 5~10%
#     
# - 하지만, 데이터 속 IVF환자 중 `PGS` `PGD` 의 비율은 1%정도이기에
#     
#     NULL값에 `PGS PGD` 검사자들이 많이 포함되어있다고 보는것이 적절
#     
#
# → 그냥 속성 삭제(?)

# + [markdown] jp-MarkdownHeadingCollapsed=true
# ##### 착상 전 유전 검사 사용 여부 칼럼 분석

# +
# PGS, PGD 시술 여부와 착상 전 유전 검사 사용 여부의 NULL 값이 일치하는 비율 계산
pgs_null = df['PGS 시술 여부'].isnull()
pgd_null = df['PGD 시술 여부'].isnull()
pre_implantation_test_null = df['착상 전 유전 검사 사용 여부'].isnull()

# 세 개의 컬럼에서 NULL 값이 동시에 존재하는 경우의 비율
all_null_match_ratio = ((pgs_null & pgd_null & pre_implantation_test_null).sum()) / len(df) * 100

# PGS와 착상 전 유전 검사 사용 여부 NULL 일치 비율
pgs_test_null_match_ratio = ((pgs_null & pre_implantation_test_null).sum()) / len(df) * 100

# PGD와 착상 전 유전 검사 사용 여부 NULL 일치 비율
pgd_test_null_match_ratio = ((pgd_null & pre_implantation_test_null).sum()) / len(df) * 100

# 결과 출력
all_null_match_ratio, pgs_test_null_match_ratio, pgd_test_null_match_ratio

# -

# `PGS` `PGD` 시술여부와 비슷한 칼럼 
#
# 3 칼럼 모두 NLL인 경우가 98% 이상
#
# 3 칼럼 모두 삭제처리

# + [markdown] jp-MarkdownHeadingCollapsed=true
# ##### 임신 시도 또는 마지막 임신 경과 연수

# +
import matplotlib.pyplot as plt

# 임신 시도 또는 마지막 임신 경과 연수가 Non-NULL인 데이터 필터링
pregnancy_attempt_non_null = df['임신 시도 또는 마지막 임신 경과 연수'].dropna()

# 0인 경우의 비중 계산
zero_ratio = (pregnancy_attempt_non_null == 0).mean() * 100

# 분포 시각화
plt.figure(figsize=(8, 5))
pregnancy_attempt_non_null.hist(bins=20, edgecolor='black')
plt.title("임신 시도 또는 마지막 임신 경과 연수 분포")
plt.xlabel("경과 연수")
plt.ylabel("빈도")
plt.show()

# 0인 경우의 비중 출력
zero_ratio

# + [markdown] jp-MarkdownHeadingCollapsed=true
# ##### 배아해동 경과일 칼럼 분석


# +
# 배아 해동 경과일이 Non-NULL인 데이터 필터링
embryo_thawing_non_null = df[df['배아 해동 경과일'].notnull()]

# 1. 시술 유형 & 특정 시술 유형 분포 확인
procedure_counts = embryo_thawing_non_null[['시술 유형', '특정 시술 유형']].value_counts()

# 2. 배아 해동 경과일의 분포 시각화
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
embryo_thawing_non_null['배아 해동 경과일'].hist(bins=20, edgecolor='black')
plt.title("배아 해동 경과일 분포")
plt.xlabel("배아 해동 경과일 (일)")
plt.ylabel("빈도")
plt.show()

# 3. 난자 해동 경과일과 배아 해동 경과일의 겹치는 경우 확인
egg_and_embryo_thawing_overlap = ((df['난자 해동 경과일'].notnull()) & (df['배아 해동 경과일'].notnull())).sum()
total_embryo_thawing_non_null = len(embryo_thawing_non_null)

# 겹치는 비율 계산
overlap_ratio = (egg_and_embryo_thawing_overlap / total_embryo_thawing_non_null) * 100

# 시술 유형 및 특정 시술 유형 출력, 겹치는 비율 출력
procedure_counts, overlap_ratio

# +
# 배아 해동 경과일이 Non-NULL인 데이터 필터링
embryo_thawing_non_null = df[df['배아 해동 경과일'].notnull()]

# 1. 동결 배아 사용 여부 분포 확인
frozen_embryo_usage_counts = embryo_thawing_non_null['동결 배아 사용 여부'].value_counts(normalize=True) * 100

# 2. 해동된 배아 수의 통계 정보 확인
thawed_embryo_counts = embryo_thawing_non_null['해동된 배아 수'].describe()

# 결과 출력
frozen_embryo_usage_counts, thawed_embryo_counts


# +
import matplotlib.pyplot as plt

# 배아 해동 경과일이 Non-NULL인 데이터 필터링
embryo_thawing_non_null = df[df['배아 해동 경과일'].notnull()]

# 1. 동결 배아 사용 여부 분포 시각화
plt.figure(figsize=(6, 4))
embryo_thawing_non_null['동결 배아 사용 여부'].value_counts().plot(kind='bar', title="동결 배아 사용 여부 분포")
plt.xlabel("동결 배아 사용 여부 (0: 사용 안함, 1: 사용)")
plt.ylabel("빈도")
plt.show()

# 2. 해동된 배아 수 분포 시각화
plt.figure(figsize=(8, 5))
embryo_thawing_non_null['해동된 배아 수'].hist(bins=40, edgecolor='black')
plt.title("해동된 배아 수 분포")
plt.xlabel("해동된 배아 수")
plt.ylabel("빈도")
plt.show()

# -

thawed_embryo_zero_ratio = (embryo_thawing_non_null['해동된 배아 수'] == 0).sum()
thawed_embryo_zero_ratio

# 동결 배아 사용 여부  나 해동된 배아 수 를 활용하여  
# 배아 동결 여부 속성 생성 후 해당 칼럼은 삭제처리

# ##### 난자 채취 경과일 칼럼 분석


