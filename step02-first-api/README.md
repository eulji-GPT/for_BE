# Step 02: 첫 번째 API

이 단계에서는 FastAPI로 간단한 API를 만들고 실행해봅니다.

## 🎯 학습 목표

- FastAPI 애플리케이션 생성
- 기본 HTTP 메서드 (GET, POST) 사용
- 자동 생성되는 API 문서 확인
- 다양한 응답 타입 처리

## 📋 단계별 진행

### 1. 애플리케이션 실행

```bash
# Step 01에서 가상환경이 활성화되어 있는지 확인
# 현재 디렉토리에서 실행
uvicorn main:app --reload
```

### 2. API 문서 확인

- 브라우저에서 `http://localhost:8000/docs` 접속 (Swagger UI)
- 또는 `http://localhost:8000/redoc` 접속 (ReDoc)

### 3. API 테스트

- 브라우저에서 `http://localhost:8000/` 접속
- 각 엔드포인트를 직접 테스트해보세요

## 🔧 실습

1. main.py 파일을 살펴보고 각 엔드포인트의 기능을 이해하세요
2. 서버를 실행하고 API 문서를 확인하세요
3. 새로운 엔드포인트를 추가해보세요

## 📚 새로운 개념

- **FastAPI 앱 인스턴스**: 모든 API의 중심이 되는 객체
- **데코레이터**: `@app.get()`, `@app.post()` 등으로 HTTP 메서드 정의
- **자동 문서화**: FastAPI가 자동으로 생성하는 API 문서
- **응답 모델**: 구조화된 JSON 응답 반환

## ✅ 다음 단계

기본 API 생성이 완료되면 Step 03으로 이동하여 경로 매개변수를 학습하세요.
