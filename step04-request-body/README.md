# Step 04: 요청 본문

이 단계에서는 POST 요청과 함께 전송되는 요청 본문을 처리하는 방법을 학습합니다.

## 🎯 학습 목표

- Pydantic 모델을 사용한 데이터 검증
- POST, PUT, PATCH 요청 처리
- 복잡한 데이터 구조 처리
- 요청 데이터 검증 및 에러 처리

## 📋 단계별 진행

### 1. Pydantic 모델 정의

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str
```

### 2. POST 엔드포인트 생성

```python
@app.post("/users/")
def create_user(user: User):
    return {"message": "사용자 생성됨", "user": user}
```

### 3. 데이터 검증

- 자동 타입 검증
- 필드 제약 조건 설정
- 커스텀 검증 규칙

## 🔧 실습

1. 서버를 실행하고 `/docs`에서 POST 요청을 테스트해보세요
2. 잘못된 데이터를 입력했을 때 어떤 오류가 발생하는지 확인하세요
3. 새로운 모델과 엔드포인트를 추가해보세요

## 📚 새로운 개념

- **Pydantic 모델**: 데이터 검증을 위한 모델 클래스
- **요청 본문**: POST/PUT 요청에 포함된 JSON 데이터
- **자동 검증**: FastAPI가 자동으로 수행하는 데이터 검증
- **응답 모델**: 응답 데이터의 구조 정의

## ✅ 다음 단계

요청 본문 처리를 익혔다면 Step 05로 이동하여 데이터베이스 연결을 학습하세요.
