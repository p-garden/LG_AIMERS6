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

# + [markdown] jp-MarkdownHeadingCollapsed=true
# # 1. 결측치 분석
# -



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

# + [markdown] jp-MarkdownHeadingCollapsed=true
# ##### 난자 채취 경과일 칼럼 분석

# +
# 난자 채취 경과일이 NULL인 데이터 필터링
egg_retrieval_null = df[df['난자 채취 경과일'].isnull()]

# 난자 채취 경과일이 NULL인 경우의 시술 유형 분포 확인
null_egg_retrieval_procedure_counts = egg_retrieval_null['시술 유형'].value_counts(normalize=True) * 100

# 결과 출력
null_egg_retrieval_procedure_counts


# +
# 난자 채취 경과일이 Non-NULL인 데이터 필터링
egg_retrieval_non_null = df[df['난자 채취 경과일'].notnull()]

# 1. 시술 유형 & 특정 시술 유형 분포 확인
procedure_counts = egg_retrieval_non_null[['시술 유형', '특정 시술 유형']].value_counts()

# 2. 난자 채취 경과일 분포 시각화
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
egg_retrieval_non_null['난자 채취 경과일'].hist(bins=20, edgecolor='black')
plt.title("난자 채취 경과일 분포")
plt.xlabel("난자 채취 경과일 (일)")
plt.ylabel("빈도")
plt.show()

# 시술 유형 및 특정 시술 유형 출력
procedure_counts


# +
# IVF 시술을 받은 경우 중 난자 채취 경과일이 NULL인 데이터 필터링
ivf_egg_retrieval_null = df[(df['시술 유형'] == 'IVF') & (df['난자 채취 경과일'].isnull())]

# IVF 시술 중 난자 채취 경과일이 NULL인 경우의 비율 계산
ivf_egg_retrieval_null_ratio = (len(ivf_egg_retrieval_null) / len(df[df['시술 유형'] == 'IVF'])) * 100

# 결과 출력
ivf_egg_retrieval_null_ratio


# +
# IVF 시술을 받은 경우 중 난자 채취 경과일이 NULL인 데이터 필터링
ivf_egg_retrieval_null = df[(df['시술 유형'] == 'IVF') & (df['난자 채취 경과일'].isnull())]
# 3가지 경우를 모두 만족하지 않는 데이터 필터링
frozen_egg = ivf_egg_retrieval_null['해동 난자 수'] >= 1  # 냉동 난자 사용 
donor_egg = ivf_egg_retrieval_null['난자 출처'] == '기증 제공'  # 기증 난자 사용 
frozen_embryo = ivf_egg_retrieval_null['동결 배아 사용 여부'] == 1  # 해동된 배아 
donor_embryo = ivf_egg_retrieval_null['기증 배아 사용 여부'] == 1  # 기증 배아 

# 4가지 경우 중 하나라도 만족하는 데이터 개수
special_case_cnt = (frozen_egg | donor_egg | frozen_embryo | donor_embryo).sum()

# 전체 IVF 중 난자 채취 경과일이 NULL인 경우 개수
total_ivf_egg_retrieval_null = len(ivf_egg_retrieval_null)

# 4가지 경우를 만족하는 비율 계산
special_case_ratio = (special_case_cnt / total_ivf_egg_retrieval_null) * 100

# 결과 출력
special_case_ratio, special_case_cnt


# +
# 4가지 경우를 모두 만족하지 않는 IVF 사례 필터링
no_special_case = ivf_egg_retrieval_null[~(frozen_egg | donor_egg | frozen_embryo | donor_embryo)]

# 남은 0.01% 사례의 개수 확인
no_special_case_count = len(no_special_case)

# 주요 특징 분석: 시술 유형, 특정 시술 유형 분포 확인
procedure_counts = no_special_case[['시술 유형', '특정 시술 유형']].value_counts()

# 주요 수치형 변수들의 통계 정보 확인
no_special_case_stats = no_special_case.describe()

# 결과 출력
no_special_case_count, procedure_counts, no_special_case_stats

# +
# IVF 시술을 받은 경우 중 난자 채취 경과일이 NULL인 데이터 필터링
ivf_egg_retrieval_null = df[(df['시술 유형'] == 'IVF') & (df['난자 채취 경과일'].isnull())]

# 각 속성 정의
frozen_egg = ivf_egg_retrieval_null['해동 난자 수'] >= 1  # 냉동 난자 사용 
donor_egg = ivf_egg_retrieval_null['난자 출처'] == '기증 제공'  # 기증 난자 사용 
frozen_embryo = ivf_egg_retrieval_null['동결 배아 사용 여부'] == 1  # 해동된 배아 사용 
donor_embryo = ivf_egg_retrieval_null['기증 배아 사용 여부'] == 1  # 기증 배아 사용 

# 중복으로 속하는 경우 확인
multi_category_cases = ivf_egg_retrieval_null[
    (frozen_egg.astype(int) + donor_egg.astype(int) + frozen_embryo.astype(int) + donor_embryo.astype(int)) > 1
]

# 중복 케이스 개수 확인
multi_category_count = len(multi_category_cases)

# 중복된 경우의 조합별 개수 확인
multi_category_combinations = multi_category_cases.apply(
    lambda row: f"{'Frozen Egg' if row['해동 난자 수'] >= 1 else ''} "
                f"{'Donor Egg' if row['난자 출처'] == '기증 제공' else ''} "
                f"{'Frozen Embryo' if row['동결 배아 사용 여부'] == 1 else ''} "
                f"{'Donor Embryo' if row['기증 배아 사용 여부'] == 1 else ''}".strip(), axis=1
).value_counts()

# 결과 출력
multi_category_count, multi_category_combinations


# +
# IVF 시술을 받은 경우 중 난자 채취 경과일이 NULL이 아닌 데이터(본인 난자 사용 가능성 있는 경우) 필터링
own_egg_cases = df[(df['시술 유형'] == 'IVF') & (df['난자 채취 경과일'].notnull())]

# 1. 본인 난자 + 외부 난자(기증 난자 또는 동결 난자) 함께 사용한 사례 확인
own_and_donor_egg = own_egg_cases['난자 출처'] == '기증 제공'  # 본인 난자 + 기증 난자 사용
own_and_frozen_egg = own_egg_cases['해동 난자 수'] >= 1  # 본인 난자 + 동결 난자 사용

mixed_egg_cases = own_egg_cases[own_and_donor_egg | own_and_frozen_egg]

# 2. 본인 배아 + 외부 배아(기증 배아 또는 동결 배아) 함께 사용한 사례 확인
own_and_donor_embryo = own_egg_cases['기증 배아 사용 여부'] == 1  # 본인 배아 + 기증 배아 사용
own_and_frozen_embryo = own_egg_cases['동결 배아 사용 여부'] == 1  # 본인 배아 + 동결 배아 사용

mixed_embryo_cases = own_egg_cases[own_and_donor_embryo | own_and_frozen_embryo]

# 개수 확인
mixed_egg_cases_count = len(mixed_egg_cases)
mixed_embryo_cases_count = len(mixed_embryo_cases)

# 조합별 분포 확인
mixed_egg_cases_distribution = mixed_egg_cases[['난자 출처', '해동 난자 수']].value_counts()
mixed_embryo_cases_distribution = mixed_embryo_cases[['동결 배아 사용 여부', '기증 배아 사용 여부']].value_counts()

# 결과 출력
mixed_egg_cases_count, mixed_egg_cases_distribution, mixed_embryo_cases_count, mixed_embryo_cases_distribution


# +
# IVF 시술을 받은 경우 필터링
ivf_cases = df[df['시술 유형'] == 'IVF'].copy()

# 각 경우의 수를 정의
ivf_cases['난자/배아 출처'] = '미정'

# 1. 본인 난자 그대로 (난자 채취 O, 외부 난자/배아 X)
ivf_cases.loc[(ivf_cases['난자 채취 경과일'].notnull()) & 
              (ivf_cases['해동 난자 수'] < 1) & 
              (ivf_cases['난자 출처'] != '기증 제공') & 
              (ivf_cases['동결 배아 사용 여부'] != 1) & 
              (ivf_cases['기증 배아 사용 여부'] != 1), '난자/배아 출처'] = '본인 난자 그대로'

# 2. 동결 난자 (해동된 난자 O, 기증 난자 X, 동결 배아 X, 기증 배아 X)
ivf_cases.loc[(ivf_cases['해동 난자 수'] >= 1) & 
              (ivf_cases['난자 출처'] != '기증 제공') & 
              (ivf_cases['동결 배아 사용 여부'] != 1) & 
              (ivf_cases['기증 배아 사용 여부'] != 1), '난자/배아 출처'] = '동결 난자'

# 3. 기증 난자 (난자 출처가 기증 제공)
ivf_cases.loc[(ivf_cases['난자 출처'] == '기증 제공') & 
              (ivf_cases['동결 배아 사용 여부'] != 1) & 
              (ivf_cases['기증 배아 사용 여부'] != 1), '난자/배아 출처'] = '기증 난자'

# 4. 동결 배아 (동결 배아 사용 O, 기증 배아 X, 난자 해동 X)
ivf_cases.loc[(ivf_cases['동결 배아 사용 여부'] == 1) & 
              (ivf_cases['기증 배아 사용 여부'] != 1) & 
              (ivf_cases['해동 난자 수'] < 1) & 
              (ivf_cases['난자 출처'] != '기증 제공'), '난자/배아 출처'] = '동결 배아'

# 5. 동결 난자 + 동결 배아
ivf_cases.loc[(ivf_cases['해동 난자 수'] >= 1) & 
              (ivf_cases['동결 배아 사용 여부'] == 1) & 
              (ivf_cases['기증 배아 사용 여부'] != 1) & 
              (ivf_cases['난자 출처'] != '기증 제공'), '난자/배아 출처'] = '동결 난자 + 동결 배아'

# 6. 본인 난자 + 배아 동결
ivf_cases.loc[(ivf_cases['난자 채취 경과일'].notnull()) & 
              (ivf_cases['동결 배아 사용 여부'] == 1) & 
              (ivf_cases['기증 배아 사용 여부'] != 1) & 
              (ivf_cases['난자 출처'] != '기증 제공'), '난자/배아 출처'] = '본인 난자 + 배아 동결'

# 7. 기증 난자 + 배아 동결
ivf_cases.loc[(ivf_cases['난자 출처'] == '기증 제공') & 
              (ivf_cases['동결 배아 사용 여부'] == 1) & 
              (ivf_cases['기증 배아 사용 여부'] != 1), '난자/배아 출처'] = '기증 난자 + 배아 동결'

# 8. 기증 난자 + 기증 배아
ivf_cases.loc[(ivf_cases['난자 출처'] == '기증 제공') & 
              (ivf_cases['기증 배아 사용 여부'] == 1), '난자/배아 출처'] = '기증 난자 + 기증 배아'

# 9. 기증 난자 + 배아 동결 + 기증 배아
ivf_cases.loc[(ivf_cases['난자 출처'] == '기증 제공') & 
              (ivf_cases['동결 배아 사용 여부'] == 1) & 
              (ivf_cases['기증 배아 사용 여부'] == 1), '난자/배아 출처'] = '기증 난자 + 배아 동결 + 기증 배아'

# 10. 동결 난자 + 기증 배아
ivf_cases.loc[(ivf_cases['해동 난자 수'] >= 1) & 
              (ivf_cases['기증 배아 사용 여부'] == 1) & 
              (ivf_cases['난자 출처'] != '기증 제공') & 
              (ivf_cases['동결 배아 사용 여부'] != 1), '난자/배아 출처'] = '동결 난자 + 기증 배아'

# 11. 본인 난자 + 외부 난자
ivf_cases.loc[(ivf_cases['난자 채취 경과일'].notnull()) & 
              (ivf_cases['난자 출처'] == '기증 제공'), '난자/배아 출처'] = '본인 난자 + 외부 난자'

# 12. 본인 배아 + 외부 배아
ivf_cases.loc[(ivf_cases['난자 채취 경과일'].notnull()) & 
              (ivf_cases['기증 배아 사용 여부'] == 1), '난자/배아 출처'] = '본인 배아 + 외부 배아'

# 13. 동결 난자 + 동결 배아 + 기증 배아
ivf_cases.loc[(ivf_cases['해동 난자 수'] >= 1) & 
              (ivf_cases['동결 배아 사용 여부'] == 1) & 
              (ivf_cases['기증 배아 사용 여부'] == 1), '난자/배아 출처'] = '동결 난자 + 동결 배아 + 기증 배아'

# 생성된 난자/배아 출처 컬럼 확인
ivf_cases['난자/배아 출처'].value_counts()

# +
# 다시 데이터 로드

# 새로운 이진(Binary) 속성 추가
df['IVF 시술 여부'] = (df['시술 유형'] == 'IVF').astype(int)  # IVF 시술 여부

df['본인 난자 사용 여부'] = df['난자 채취 경과일'].notnull().astype(int)  # 본인 난자 사용 여부
df['동결 난자 사용 여부'] = (df['해동 난자 수'] >= 1).astype(int)  # 동결 난자 사용 여부
df['기증 난자 사용 여부'] = (df['난자 출처'] == '기증 제공').astype(int)  # 기증 난자 사용 여부

df['자연 배아 사용 여부'] = df['난자 채취 경과일'].notnull().astype(int)  # 본인 배아 사용 여부
df['동결 배아 사용 여부'] = (df['동결 배아 사용 여부'] == 1).astype(int)  # 동결 배아 사용 여부
df['기증 배아 사용 여부'] = (df['기증 배아 사용 여부'] == 1).astype(int)  # 기증 배아 사용 여부

# 새롭게 추가된 이진 컬럼 확인
binary_columns = ['IVF 시술 여부', '본인 난자 사용 여부', '동결 난자 사용 여부', '기증 난자 사용 여부',
                  '자연 배아 사용 여부', '동결 배아 사용 여부', '기증 배아 사용 여부']

binary_summary = df[binary_columns].sum().reset_index()
binary_summary.columns = ['속성', '사용된 사례 수']

binary_summary
# -
# ##### 난자혼합경과일 칼럼 분석

# +

# 난자 혼합 경과일 분포 확인
egg_mixing_days_distribution = df['난자 혼합 경과일'].describe()

# 난자 혼합 경과일의 시술 유형 분포 확인 (IVF 여부)
egg_mixing_by_treatment = df.groupby('시술 유형')['난자 혼합 경과일'].count()

# 난자 혼합 경과일과 난자 출처 관계 분석
egg_mixing_vs_source = df.groupby('난자 출처')['난자 혼합 경과일'].describe()

# 결과 출력
egg_mixing_days_distribution, egg_mixing_by_treatment, egg_mixing_vs_source


# +
# 난자 혼합 경과일이 4일 이상인 데이터 개수 확인
egg_mixing_above_4_days = df[df['난자 혼합 경과일'] >= 4].shape[0]

# 결과 출력
egg_mixing_above_4_days

# -



# +
# 1. 분포 확인
embryo_transfer_days_distribution = df['배아 이식 경과일'].describe()

# 2. 시술 유형과 관계 분석 (IVF 여부)
embryo_transfer_by_treatment = df.groupby('시술 유형')['배아 이식 경과일'].count()

# 3. 배아 이식 경과일과 배아 출처 관계 분석
embryo_transfer_vs_source = df.groupby('난자 출처')['배아 이식 경과일'].describe()

# 결과 출력
embryo_transfer_days_distribution, embryo_transfer_by_treatment, embryo_transfer_vs_source
# -

# ##### 배아이식경과일 칼럼 분석

# +
# 1. 분포 확인
embryo_transfer_days_distribution = df['배아 이식 경과일'].describe()

# 2. 시술 유형과 관계 분석 (IVF 여부)
embryo_transfer_by_treatment = df.groupby('시술 유형')['배아 이식 경과일'].count()

# 3. 배아 이식 경과일과 배아 출처 관계 분석
embryo_transfer_vs_source = df.groupby('난자 출처')['배아 이식 경과일'].describe()

# 결과 출력
embryo_transfer_days_distribution, embryo_transfer_by_treatment, embryo_transfer_vs_source

# +
# 배아 이식 경과일의 결측치 개수 확인
missing_embryo_transfer_days = df['배아 이식 경과일'].isnull().sum()

# 시술 당시 나이별 중앙값 확인
age_group_median_check = df.groupby('시술 당시 나이')['배아 이식 경과일'].median()

# 결과 출력
missing_embryo_transfer_days, age_group_median_check

# -

# ##### 총 생성 배아 수 칼럼 분석

# # 2. 각 칼럼별 의미

# ##### 시술 시기 코드

# +
# 데이터 다
# 시술 유형을 숫자로 변환 (DI = 0, IVF = 1)
df['IVF 시술 여부'] = (df['시술 유형'] == 'IVF').astype(int)

# 1. 시술 시기 코드별 빈도 분석
treatment_code_counts = df['시술 시기 코드'].value_counts()

# 2. 시술 시기 코드별 시술 당시 나이 분포 확인 (범주형 변수이므로 비율 분석)
treatment_code_age_distribution = df.groupby('시술 시기 코드')['시술 당시 나이'].value_counts(normalize=True).unstack()

# 3. 시술 시기 코드별 IVF 시술 비율 확인 (IVF 시술 여부 평균 계산)
treatment_code_ivf_ratio = df.groupby('시술 시기 코드')['IVF 시술 여부'].mean()

# 결과 출력
treatment_code_counts, treatment_code_age_distribution, treatment_code_ivf_ratio


# +
# 시술 시기 코드별 임신 성공 여부 평균 (타겟값과의 관계 확인)
treatment_code_pregnancy_rate = df.groupby('시술 시기 코드')['임신 성공 여부'].mean().sort_values(ascending=False)

# 결과 출력
treatment_code_pregnancy_rate

# -

# ##### 시술 당시 나이

# +

# 시술 유형을 숫자로 변환 (DI = 0, IVF = 1)
df['IVF 시술 여부'] = (df['시술 유형'] == 'IVF').astype(int)

# 1. 시술 당시 나이 분포 확인
age_distribution = df['시술 당시 나이'].value_counts(normalize=True).sort_index()

# 2. 시술 당시 나이별 임신 성공 여부 평균 (타깃값과의 관계 확인)
age_pregnancy_rate = df.groupby('시술 당시 나이')['임신 성공 여부'].mean().sort_index()

# 3. 시술 유형별 임신 성공률 분석
age_treatment_distribution = df.groupby('시술 당시 나이')['시술 유형'].value_counts(normalize=True).unstack()

# 결과 출력
age_distribution, age_pregnancy_rate, age_treatment_distribution

# -
# ##### 시술 유형 - 특정 시술 유형


# +
# 1. 시술 유형 분포 확인
treatment_distribution = df['시술 유형'].value_counts(normalize=True)

# 2. 특정 시술 유형 분포 확인 (특정 시술 유형 칼럼이 있는 경우)
if '특정 시술 유형' in df.columns:
    specific_treatment_distribution = df['특정 시술 유형'].value_counts(normalize=True)
else:
    specific_treatment_distribution = "특정 시술 유형 컬럼이 존재하지 않습니다."

# 결과 출력
treatment_distribution, specific_treatment_distribution


# +
# 1. 시술 유형별 개수 및 비율 확인
treatment_distribution = df['시술 유형'].value_counts(normalize=True)

# 2. 시술 유형별 특정 시술 유형 분포 확인
specific_treatment_by_type = df.groupby('시술 유형')['특정 시술 유형'].value_counts(normalize=True).unstack()

# 결과 출력
treatment_distribution, specific_treatment_by_type


# +
# 특정 시술 유형별 타깃값(임신 성공 여부) 평균 계산
specific_treatment_pregnancy_rate = df.groupby('특정 시술 유형')['임신 성공 여부'].mean().sort_values(ascending=False)

# 특정 시술 유형별 연령대(시술 당시 나이) 분포 확인
specific_treatment_age_distribution = df.groupby('특정 시술 유형')['시술 당시 나이'].value_counts(normalize=True).unstack()

# 결과 출력
specific_treatment_pregnancy_rate, specific_treatment_age_distribution

# -

# ##### 배란 자극 여부

# +
# 배란 자극 여부 칼럼 분석

# 1. 배란 자극 여부 분포 확인
ovulation_stimulation_distribution = df['배란 자극 여부'].value_counts(normalize=True)

# 2. 배란 자극 여부별 임신 성공률 분석
ovulation_stimulation_pregnancy_rate = df.groupby('배란 자극 여부')['임신 성공 여부'].mean()

# 3. 배란 자극 여부별 시술 유형 분석
ovulation_stimulation_treatment_distribution = df.groupby('배란 자극 여부')['시술 유형'].value_counts(normalize=True).unstack()

# 결과 출력
ovulation_stimulation_distribution, ovulation_stimulation_pregnancy_rate, ovulation_stimulation_treatment_distribution

# -

# ##### 배란 유도 유형

# +
# 배란 유도 유형 칼럼 분석

# 1. 배란 유도 유형 분포 확인
ovulation_induction_distribution = df['배란 유도 유형'].value_counts(normalize=True)

# 2. 배란 유도 유형별 임신 성공률 분석
ovulation_induction_pregnancy_rate = df.groupby('배란 유도 유형')['임신 성공 여부'].mean().sort_values(ascending=False)

# 3. 배란 유도 유형별 시술 유형 분석
ovulation_induction_treatment_distribution = df.groupby('배란 유도 유형')['시술 유형'].value_counts(normalize=True).unstack()

# 결과 출력
ovulation_induction_distribution, ovulation_induction_pregnancy_rate, ovulation_induction_treatment_distribution

# -

# ##### 단일 배아 이식 여부

# +

# 1. 단일 배아 이식 여부 분포 확인
single_embryo_transfer_distribution = df['단일 배아 이식 여부'].value_counts(normalize=True)

# 2. 단일 배아 이식 여부별 임신 성공률 분석
single_embryo_pregnancy_rate = df.groupby('단일 배아 이식 여부')['임신 성공 여부'].mean()

# 3. 단일 배아 이식 여부별 시술 유형 분석
single_embryo_treatment_distribution = df.groupby('단일 배아 이식 여부')['시술 유형'].value_counts(normalize=True).unstack()

# 결과 출력
single_embryo_transfer_distribution, single_embryo_pregnancy_rate, single_embryo_treatment_distribution

# -


