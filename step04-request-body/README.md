# Step 04: 요청 본문 - 을지대학교 을GPT

을지대학교 을GPT 프로젝트에서 POST 요청과 함께 전송되는 요청 본문을 처리하는 방법을 학습합니다.

## 🎯 학습 목표

- 을지대학교 을GPT 프로젝트에서 Pydantic 모델을 사용한 데이터 검증
- 을지대학교 학생 및 프로젝트 데이터에 대한 POST, PUT, PATCH 요청 처리
- 을지대학교 을GPT 복잡한 데이터 구조 처리
- 을지대학교 을GPT 요청 데이터 검증 및 에러 처리

## 📋 단계별 진행

### 1. 을지대학교 을GPT Pydantic 모델 정의

```python
# 을지대학교 전공 열거형
class EuljiMajor(str, Enum):
    nursing = "간호학과"
    radiology = "방사선학과"
    medical_it = "의료IT학과"
    physical_therapy = "물리치료학과"

# 을지대학교 학생 모델
class EuljiStudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="학생 이름")
    email: EmailStr = Field(..., description="이메일 주소")
    student_id: str = Field(..., min_length=8, max_length=12, description="학번")
    major: EuljiMajor = Field(..., description="전공")
    grade: int = Field(..., ge=1, le=4, description="학년")
```

### 2. 을지대학교 을GPT POST 엔드포인트 생성

```python
@app.post("/students/")
def create_eulji_student(student: EuljiStudentCreate):
    return {"message": "을지대학교 학생 생성됨", "student": student}
```

### 3. 을지대학교 을GPT 데이터 검증

- 을지대학교 학번 자동 타입 검증
- 을지대학교 전공별 필드 제약 조건 설정
- 을지대학교 을GPT 커스텀 검증 규칙

## 🔧 을지대학교 을GPT 실습

1. 을지대학교 을GPT 서버를 실행하고 `/docs`에서 POST 요청을 테스트해보세요
2. 을지대학교 학생 데이터에 잘못된 정보를 입력했을 때 어떤 오류가 발생하는지 확인하세요
3. 을지대학교 을GPT 새로운 모델과 엔드포인트를 추가해보세요

## 📚 을지대학교 을GPT 새로운 개념

- **을지대학교 을GPT Pydantic 모델**: 을지대학교 학생 데이터 검증을 위한 모델 클래스
- **을지대학교 을GPT 요청 본문**: POST/PUT 요청에 포함된 을지대학교 학생 JSON 데이터
- **을지대학교 을GPT 자동 검증**: FastAPI가 자동으로 수행하는 을지대학교 데이터 검증
- **을지대학교 을GPT 응답 모델**: 을지대학교 을GPT 응답 데이터의 구조 정의

## ✅ 다음 단계

요청 본문 처리를 익혔다면 Step 05로 이동하여 데이터베이스 연결을 학습하세요.
