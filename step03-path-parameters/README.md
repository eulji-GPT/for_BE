# Step 03: 경로 매개변수 - 을지대학교 을GPT

을지대학교 을GPT 프로젝트에서 동적 경로 매개변수를 사용하여 더 유연하고 강력한 API를 만들어봅니다.

## 🎯 학습 목표

- 을지대학교 을GPT 프로젝트에서 경로 매개변수 사용법 완전 이해
- 을지대학교 학생 및 프로젝트 데이터에 대한 매개변수 타입 지정 및 고급 검증
- 을지대학교 을GPT 여러 매개변수 조합 및 복잡한 경로 구성
- 을지대학교 을GPT 경로 매개변수 제약 조건 설정
- HTTPException을 활용한 에러 처리
- 을지대학교 을GPT 실제 데이터를 활용한 CRUD 기본 연산

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
# Step 03 디렉토리로 이동
cd step03-path-parameters

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

### 3. 을지대학교 을GPT 주요 엔드포인트 테스트

**을지대학교 을GPT 기본 엔드포인트들:**
- 을지대학교 을GPT 루트: `http://localhost:8000/`
- 을지대학교 학생 조회: `http://localhost:8000/students/1`
- 을지대학교 프로젝트 조회: `http://localhost:8000/projects/1`
- 을지대학교 을GPT 인사말: `http://localhost:8000/greet/김을지`

**고급 엔드포인트들:**
- 계산기: `http://localhost:8000/calculate/multiply/12/8`
- 카테고리별 제품: `http://localhost:8000/categories/컴퓨터/products`
- 사용자 프로필: `http://localhost:8000/users/1/profile?include_details=true`
- 나이 그룹별 조회: `http://localhost:8000/users/age-group/25/30`
- 파일 경로: `http://localhost:8000/files/documents/report.pdf`

### 4. API 문서 확인

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔧 실습

1. **환경 설정**: 아나콘다 환경을 활성화하고 서버를 실행하세요
2. **기본 테스트**: 사용자 및 제품 조회 엔드포인트를 테스트하세요
3. **고급 테스트**: 계산기와 카테고리별 조회 기능을 테스트하세요
4. **에러 처리**: 존재하지 않는 ID나 잘못된 매개변수로 에러 응답을 확인하세요
5. **새로운 엔드포인트**: 본인만의 경로 매개변수 엔드포인트를 추가해보세요

## 🌐 테스트 방법

### 1. 웹 브라우저에서 테스트
직접 URL을 입력하여 GET 요청을 테스트할 수 있습니다.

### 2. PowerShell에서 테스트
```bash
# 사용자 정보 조회
Invoke-RestMethod -Uri "http://localhost:8000/users/1" -Method GET

# 제품 정보 조회
Invoke-RestMethod -Uri "http://localhost:8000/products/1" -Method GET

# 인사말 테스트
Invoke-RestMethod -Uri "http://localhost:8000/greet/홍길동" -Method GET

# 계산기 테스트
Invoke-RestMethod -Uri "http://localhost:8000/calculate/multiply/12/8" -Method GET

# 카테고리별 제품 조회
Invoke-RestMethod -Uri "http://localhost:8000/categories/컴퓨터/products" -Method GET

# 나이 그룹별 사용자 조회
Invoke-RestMethod -Uri "http://localhost:8000/users/age-group/25/30" -Method GET
```

### 3. Swagger UI에서 테스트
- `http://localhost:8000/docs`에서 각 엔드포인트를 직접 테스트할 수 있습니다
- 매개변수 검증 조건도 자동으로 문서화됩니다

## 📚 새로운 개념

### 1. 경로 매개변수 기본 사용법
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### 2. 매개변수 타입 지정
- `int`: 정수 (예: `/users/1`)
- `float`: 실수 (예: `/calculate/add/10.5/2.3`)
- `str`: 문자열 (예: `/greet/홍길동`)
- `bool`: 불리언 (쿼리 매개변수로 주로 사용)

### 3. 매개변수 검증 (Path 사용)
```python
from fastapi import Path

@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., gt=0, description="사용자 ID")):
    return {"user_id": user_id}
```

**검증 조건:**
- `gt`: 초과 (greater than)
- `ge`: 이상 (greater than or equal)
- `lt`: 미만 (less than)
- `le`: 이하 (less than or equal)
- `min_length`: 최소 길이 (문자열)
- `max_length`: 최대 길이 (문자열)

### 4. 여러 매개변수 조합
```python
@app.get("/calculate/{operation}/{num1}/{num2}")
def calculate(operation: str, num1: float, num2: float):
    # 여러 매개변수를 동시에 사용
    pass
```

### 5. 경로 매개변수와 쿼리 매개변수 조합
```python
@app.get("/users/{user_id}/profile")
def get_profile(user_id: int, include_details: bool = False):
    # 경로 매개변수 + 쿼리 매개변수
    pass
```

### 6. 에러 처리
```python
from fastapi import HTTPException

if user_id not in users:
    raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
```

## � 코드 분석

### 샘플 데이터
- **사용자 데이터**: 3명의 사용자 정보 (홍길동, 김철수, 이영희)
- **제품 데이터**: 3개의 제품 정보 (노트북, 마우스, 키보드)

### 주요 엔드포인트들

1. **사용자 조회** (`/users/{user_id}`): ID로 특정 사용자 조회
2. **제품 조회** (`/products/{product_id}`): ID로 특정 제품 조회
3. **인사말** (`/greet/{name}`): 이름을 받아 개인화된 인사말 생성
4. **계산기** (`/calculate/{operation}/{num1}/{num2}`): 4가지 연산 수행
5. **사용자 프로필** (`/users/{user_id}/profile`): 상세 정보 포함 옵션
6. **파일 경로** (`/files/{file_path:path}`): 파일 경로 처리
7. **카테고리별 제품** (`/categories/{category}/products`): 카테고리로 필터링
8. **나이 그룹별 사용자** (`/users/age-group/{min_age}/{max_age}`): 나이 범위로 검색

## 🐛 자주 발생하는 이슈

### 1. 타입 오류
```
422 Unprocessable Entity
```
- 숫자가 와야 할 곳에 문자열을 입력한 경우
- 예: `/users/abc` (user_id는 int여야 함)

### 2. 존재하지 않는 리소스
```
404 Not Found
```
- 존재하지 않는 사용자 ID나 제품 ID를 조회할 때
- 예: `/users/999` (존재하지 않는 사용자)

### 3. 검증 조건 위반
```
422 Unprocessable Entity
```
- Path 검증 조건을 위반했을 때
- 예: `/users/0` (gt=0 조건 위반)

### 4. 잘못된 연산
```
400 Bad Request
```
- 지원하지 않는 연산자 사용
- 0으로 나누기 시도

## 🎯 실제 테스트 결과

### 성공 테스트
```json
// GET /users/1 응답
{
  "user": {
    "id": 1,
    "name": "홍길동",
    "age": 30,
    "city": "서울"
  }
}

// GET /calculate/multiply/12/8 응답
{
  "operation": "multiply",
  "operand1": 12.0,
  "operand2": 8.0,
  "result": 96.0
}

// GET /categories/컴퓨터/products 응답
{
  "category": "컴퓨터",
  "products": [
    {"id": 2, "name": "마우스", "price": 25000, "category": "컴퓨터"},
    {"id": 3, "name": "키보드", "price": 80000, "category": "컴퓨터"}
  ],
  "count": 2
}
```
## 📚 참고 자료

- [FastAPI 경로 매개변수 가이드](https://fastapi.tiangolo.com/tutorial/path-params/)
- [경로 매개변수 검증](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/)
- [HTTP 상태 코드](https://fastapi.tiangolo.com/tutorial/response-status-code/)
- [에러 처리](https://fastapi.tiangolo.com/tutorial/handling-errors/)

## ✅ 다음 단계

Step 03이 완료되면 Step 04로 이동하여 요청 본문(Request Body)을 학습하세요.

**성공 확인 체크리스트:**
- [ ] 아나콘다 환경에서 서버 실행 성공
- [ ] 기본 경로 매개변수 테스트 완료 (사용자, 제품 조회)
- [ ] 문자열 경로 매개변수 테스트 완료 (인사말)
- [ ] 여러 매개변수 조합 테스트 완료 (계산기)
- [ ] 경로 + 쿼리 매개변수 조합 테스트 완료 (사용자 프로필)
- [ ] 카테고리별 제품 조회 테스트 완료
- [ ] 나이 그룹별 사용자 조회 테스트 완료
- [ ] 에러 처리 확인 완료 (404, 422, 400 에러)
- [ ] Swagger UI에서 API 문서 확인 완료
- [ ] 매개변수 검증 조건 이해 완료

**고급 학습 포인트:**
- 경로 매개변수 순서의 중요성 이해
- 정적 경로 vs 동적 경로 우선순위
- 복잡한 경로 구조 설계 원칙
- RESTful API 설계 패턴 적용