# Step 02: 첫 번째 API - 을지대학교 을GPT

을지대학교 을GPT 프로젝트의 FastAPI로 간단한 API를 만들고 실행해봅니다.

## 🎯 학습 목표

- 을지대학교 을GPT FastAPI 애플리케이션 생성 및 실행
- 다양한 HTTP 메서드 (GET, POST) 사용법
- 경로 매개변수와 동적 라우팅 구현
- 을지대학교 을GPT 프로젝트에 특화된 API 문서 확인 및 활용
- 다양한 응답 타입 처리 및 에러 핸들링

## 📋 단계별 진행

### 1. 을지대학교 을GPT 아나콘다 환경 설정

```bash
# 사용 가능한 conda 환경 확인
conda info --envs

# 을지대학교 을GPT 전용 환경 활성화
conda activate Python3.11-eulGPT-Backend
```

### 2. 을지대학교 을GPT 애플리케이션 실행

```bash
# Step 02 디렉토리로 이동
cd step02-first-api

# 을지대학교 을GPT FastAPI 애플리케이션 실행
python main.py
```

실행 성공 시 다음과 같은 메시지가 표시됩니다:
```
INFO:     Started server process [프로세스ID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 3. 을지대학교 을GPT API 문서 확인

- **을지대학교 을GPT Swagger UI**: `http://localhost:8000/docs`
- **을지대학교 을GPT ReDoc**: `http://localhost:8000/redoc`
- 이 문서들을 통해 을지대학교 을GPT 각 엔드포인트를 직접 테스트할 수 있습니다

### 4. 을지대학교 을GPT 엔드포인트 테스트

**을지대학교 을GPT 기본 엔드포인트들:**
- 을지대학교 을GPT 루트: `http://localhost:8000/`
- 을지대학교 을GPT 인사말: `http://localhost:8000/hello`
- 을지대학교 을GPT 서버 시간: `http://localhost:8000/time`
- 을지대학교 을GPT 서버 정보: `http://localhost:8000/info`

**을지대학교 을GPT 계산기 엔드포인트 (경로 매개변수 사용):**
- 덧셈: `http://localhost:8000/calculate/add/10/5`
- 뺄셈: `http://localhost:8000/calculate/subtract/10/5`
- 곱셈: `http://localhost:8000/calculate/multiply/10/5`
- 나눗셈: `http://localhost:8000/calculate/divide/10/5`

**을지대학교 을GPT POST 엔드포인트:**
- 메시지 에코: `http://localhost:8000/echo` (POST 요청)

## 🔧 을지대학교 을GPT 실습

1. **을지대학교 을GPT 코드 분석**: main.py 파일을 살펴보고 각 엔드포인트의 기능을 이해하세요
2. **을지대학교 을GPT 서버 실행**: 아나콘다 환경을 활성화하고 애플리케이션을 실행하세요
3. **을지대학교 을GPT API 문서 확인**: Swagger UI와 ReDoc에서 자동 생성된 문서를 확인하세요
4. **을지대학교 을GPT 엔드포인트 테스트**: 각 API를 직접 호출해보고 응답을 확인하세요
5. **을지대학교 을GPT 새로운 엔드포인트 추가**: 본인만의 API 엔드포인트를 추가해보세요

## 🌐 을지대학교 을GPT 테스트 방법

### 1. 웹 브라우저에서 을지대학교 을GPT 테스트
직접 URL을 입력하여 GET 요청을 테스트할 수 있습니다.

### 2. PowerShell에서 을지대학교 을GPT 테스트
```bash
# 을지대학교 을GPT 기본 엔드포인트 테스트
Invoke-RestMethod -Uri "http://localhost:8000/hello" -Method GET

# 을지대학교 을GPT 계산기 엔드포인트 테스트
Invoke-RestMethod -Uri "http://localhost:8000/calculate/add/15/25" -Method GET

# 을지대학교 을GPT POST 엔드포인트 테스트
$body = @{message="을지대학교 을GPT 테스트"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/echo" -Method POST -Body $body -ContentType "application/json"
```

### 3. 을지대학교 을GPT Swagger UI에서 테스트
- `http://localhost:8000/docs`에서 각 엔드포인트의 "Try it out" 버튼을 클릭
- 필요한 매개변수를 입력하고 실행해보세요

## 📚 을지대학교 을GPT 새로운 개념

- **을지대학교 을GPT FastAPI 앱 인스턴스**: 모든 API의 중심이 되는 객체
- **데코레이터**: `@app.get()`, `@app.post()` 등으로 HTTP 메서드 정의
- **경로 매개변수**: URL에 포함된 동적 값들 (`/calculate/{operation}/{a}/{b}`)
- **자동 문서화**: FastAPI가 자동으로 생성하는 API 문서
- **응답 모델**: 구조화된 JSON 응답 반환
- **에러 핸들링**: 0으로 나누기 등의 예외 상황 처리

## 🔍 코드 분석

### 주요 엔드포인트들:

1. **루트 엔드포인트** (`/`): 기본 환영 메시지
2. **인사말 엔드포인트** (`/hello`): 한국어 메시지 포함
3. **시간 엔드포인트** (`/time`): 현재 시간과 타임스탬프
4. **서버 정보** (`/info`): 서버 상태와 사용 가능한 엔드포인트 목록
5. **계산기** (`/calculate/{operation}/{a}/{b}`): 동적 경로 매개변수 사용
6. **에코 API** (`/echo`): POST 요청으로 전달받은 데이터 반환

## 🐛 자주 발생하는 이슈

### 1. 포트 충돌
```
OSError: [Errno 98] Address already in use
```
- 8000 포트가 이미 사용 중입니다
- 기존 서버를 종료하거나 다른 포트를 사용하세요

### 2. 계산기 에러
- 0으로 나누기 시도: `{"error": "Division by zero is not allowed"}`
- 잘못된 연산자: `{"error": "Invalid operation"}`

### 3. POST 요청 형식 오류
- Content-Type이 `application/json`인지 확인하세요
- 요청 본문이 올바른 JSON 형식인지 확인하세요

## 📚 참고 자료

- [FastAPI 라우팅 가이드](https://fastapi.tiangolo.com/tutorial/path-params/)
- [HTTP 메서드 정의](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [자동 API 문서화](https://fastapi.tiangolo.com/tutorial/metadata/)

## ✅ 다음 단계

Step 02가 완료되면 Step 03으로 이동하여 경로 매개변수를 더 자세히 학습하세요.

**성공 확인 체크리스트:**
- [ ] 아나콘다 환경에서 서버 실행 성공
- [ ] 모든 GET 엔드포인트 테스트 완료
- [ ] 계산기 기능 (4가지 연산) 테스트 완료
- [ ] POST 엔드포인트 테스트 완료
- [ ] Swagger UI에서 API 문서 확인 완료
- [ ] 에러 핸들링 (0으로 나누기 등) 확인 완료

**테스트 완료 예시:**
```json
// GET /hello 응답
{
  "greeting": "Hello",
  "message": "FastAPI로 만든 첫 번째 API입니다!"
}

// GET /calculate/add/15/25 응답
{
  "operation": "add",
  "operand1": 15.0,
  "operand2": 25.0,
  "result": 40.0
}
```
