# 🧠 My Tutoring Box - 머신러닝 기반 학생 유형 분류기

과외 통합 관리 웹 애플리케이션에서 사용할 머신러닝 모델을 개발하기 위한 Python 기반 분류 시스템입니다.  
학생의 수학 모의고사 정오표 데이터를 기반으로 학습 유형을 분류하고, 이에 따라 맞춤형 교재 추천이 가능하도록 설계되었습니다.

---

## 📁 프로젝트 구조

```
MY-TUTORING-BOX-ML/
├── app/
│   ├── __init__.py
│   ├── loader.py              # 모델 로딩 전용 유틸
│   ├── predict.py             # FastAPI 라우터
│   ├── schemas.py             # Pydantic 모델
│   └── train_model.py         # 학습 + 데이터 생성
│
├── data/
│   ├── train.csv              # 학습 데이터 (80%)
│   └── test.csv               # 테스트 데이터 (20%)
│
├── model/
│   └── student_type_classifier_100k.pkl   # 저장된 모델
│
├── venv/                      # 가상환경 (Git 관리 제외)
│
├── .gitignore                 # venv, __pycache__, .pkl 제외
├── main.py                    # FastAPI 진입점
├── test_model.py              # 예측 기능 단독 테스트
├── requirements.txt           # 의존성 목록
└── README.md                  # 프로젝트 설명서
```

---

## 🔧 사용 방법

### 1. 가상환경 구성

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 모델 학습 및 저장

```bash
python app/train_model.py
```

### 4. 예측 테스트

```bash
python test_model.py
```

---

## 🚀 FastAPI 예측 서버 실행

```bash
uvicorn main:app --reload
```

서버가 `http://localhost:8000` 에서 실행되고,  
`/predict` 엔드포인트로 POST 요청 시 예측 결과를 반환합니다.

**요청 예시**

```json
POST http://localhost:8000/predict
{
  "answers": [1, 0, 1, 1, 0, ..., 1]  // 총 30개
}
```

**응답 예시**

```json
{
  "label": 2,
  "type": "킬러 취약형"
}
```

---

## 🤝 NestJS 연동 방법

NestJS에서 FastAPI 머신러닝 서버에 HTTP 요청을 보내 예측 결과를 받을 수 있습니다.

### 1️⃣ axios 설치

```bash
npm install axios
```

### 2️⃣ `ml.service.ts`

```ts
import { Injectable } from "@nestjs/common";
import axios from "axios";

@Injectable()
export class MlService {
  async predictStudentType(answers: number[]): Promise<any> {
    const url = "http://localhost:8000/predict";

    const response = await axios.post(url, { answers });
    return response.data; // { label: 2, type: "킬러 취약형" }
  }
}
```

### 3️⃣ `ml.controller.ts`

```ts
import { Controller, Post, Body } from "@nestjs/common";
import { MlService } from "./ml.service";

@Controller("ml")
export class MlController {
  constructor(private readonly mlService: MlService) {}

  @Post("predict")
  async predict(@Body("answers") answers: number[]) {
    return await this.mlService.predictStudentType(answers);
  }
}
```

### 4️⃣ 모듈 등록

```ts
@Module({
  controllers: [MlController],
  providers: [MlService],
})
export class MlModule {}
```

---

## 📈 예측 예시 결과

```
👤 학생 1: 라벨 = 2, 유형 = 킬러 취약형
👤 학생 2: 라벨 = 0, 유형 = 개념 부족형
```

---

## 🧪 향후 개선 방향

- 실제 학생 응답 기반 데이터로 모델 파인튜닝
- 과목 확장 (현재는 수학만 지원)
- 문제별 주제 및 단원 정보 기반 원인 분석 추가
- ChatGPT API 연동을 통한 실시간 피드백 기능 등

---

## 📌 개발 환경

- Python 3.8+
- scikit-learn
- FastAPI
- Uvicorn
- NestJS (TypeScript, axios)

---

## 👨‍💻 Maintainer

- 개발자: 박지연
- 프로젝트명: My Tutoring Box
- 목적: 머신러닝 기반 학생 맞춤형 학습 지원 시스템
