# 🚀 LG AIMERS 6기 해커톤 - 난임 환자 임신 성공 여부 예측 AI
## 🎯 오프라인 해커톤 진출 성공
## 🎉 29등 / 794팀 (상위 100명 내 오프라인 진출)
## 💡 AutoML과 Feature Engineering으로 최적의 모델 구축
![image](https://github.com/user-attachments/assets/2051fc25-298a-4058-a781-8b741fb176c3)

### 🔥 핵심 목표:
	•	Feature Engineering을 통해 유의미한 속성 생성
	•	AutoML을 활용한 최적의 모델 탐색
	•	앙상블 기법을 통해 성능 극대화및 과적합 방지


### 🔍 접근 방법
#### 1️⃣ Feature Engineering
  67개의 속성이 존재했으며, 중요한 피처를 선별하여 최적의 모델 성능을 이끌어냄.  
  ✔ Feature Importance & p-value 분석:  
  	•	feature_importance가 낮거나 p-value가 높은 속성 제거 (다중공선성 해결)  
  ✔ Feature Engineering:  
  	•	중요한 속성을 활용하여 파생 변수 생성  
  	•	파생 변수를 모델에 적용 후, feature_importance가 높아졌는지 검증  
#### 2️⃣ 모델링 - AutoML (AutoGluon 활용)  
  💡 AutoGluon을 활용하여 모델을 자동 탐색 및 튜닝    
  ✔ 앙상블 전략 최적화      
  	•	CatBoost 성능이 특히 좋았지만, 특정 모델이 과도하게 포함되지 않도록 조절  
  	•	다양한 모델이 골고루 섞인 앙상블 모델 구축  
  ✔ 적절한 하이퍼파라미터 설정 -> 가벼운 모델 제작  
  	•	time_limit, bagging 등 파라미터들을 가볍게 설정하여 과적합 방지  


### 📌 참고 자료 & 링크
📂 프로젝트 회고록 : 🔗 https://velog.io/@j2982477/LG-AIMERS-6%EA%B8%B0-%EC%98%A8%EB%9D%BC%EC%9D%B8-%ED%95%B4%EC%BB%A4%ED%86%A4-%ED%9B%84%EA%B8%B0-%EC%98%A4%ED%94%84%EB%9D%BC%EC%9D%B8-%EC%A7%84%EC%B6%9C



  	
