# Step 04: 요청 본문 - 을지대학교 을GPT

을지대학교 을GPT 프로젝트에서 Pydantic 모델을 사용한 요청 본문 처리와 데이터 검증을 학습합니다.

## 🎯 학습 목표

- 을지대학교 을GPT 프로젝트에 맞는 Pydantic 모델 설계
- 을지대학교 학생, 프로젝트, 팀 데이터 관리
- 복잡한 데이터 구조와 중첩된 모델 처리
- 요청 데이터 검증 및 커스텀 에러 처리

## 📋 을지대학교 을GPT 프로젝트 구조

### 1. 을지대학교 전공 및 역할 정의

```python
# 을지대학교 전공 열거형
class EuljiMajor(str, Enum):
    nursing = "nursing"              # 간호학과
    radiology = "radiology"          # 방사선학과
    medical_it = "medical_it"        # 의료IT학과
    physical_therapy = "physical_therapy"  # 물리치료학과

# 학생 역할 열거형
class StudentRole(str, Enum):
    student = "student"     # 학생
    admin = "admin"         # 관리자
    professor = "professor" # 교수
    assistant = "assistant" # 조교
```

### 2. 을지대학교 학생 모델

```python
class EuljiStudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="학생 이름")
    email: EmailStr = Field(..., description="이메일 주소")
    student_id: str = Field(..., min_length=8, max_length=12, description="학번")
    major: EuljiMajor = Field(..., description="전공")
    grade: int = Field(..., ge=1, le=4, description="학년")
    role: StudentRole = Field(default=StudentRole.student, description="역할")

class EuljiStudentCreate(EuljiStudentBase):
    password: str = Field(..., min_length=8, description="비밀번호")
    confirm_password: str = Field(..., description="비밀번호 확인")
```

### 3. 을지대학교 을GPT 프로젝트 모델

```python
class EuljiProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="프로젝트명")
    description: Optional[str] = Field(None, max_length=1000, description="프로젝트 설명")
    category: ProjectCategory = Field(..., description="카테고리")
    team_size: int = Field(..., gt=0, le=10, description="팀 크기")
```

## 🚀 서버 실행

```bash
# 패키지 설치
pip install fastapi uvicorn pydantic email-validator

# 서버 실행
python main.py

# 또는 uvicorn 직접 실행
uvicorn main:app --reload --port 8000
```

## 🌐 API 문서 및 테스트

- **API 문서**: http://localhost:8000/docs
- **대안 문서**: http://localhost:8000/redoc
- **기본 홈페이지**: http://localhost:8000

## 📊 주요 엔드포인트

### 학생 관리
- `POST /students/` - 새 학생 등록
- `GET /students/` - 학생 목록 조회
- `GET /students/{student_id}` - 특정 학생 조회
- `PUT /students/{student_id}` - 학생 정보 수정

### 프로젝트 관리
- `POST /projects/` - 새 프로젝트 생성
- `GET /projects/` - 프로젝트 목록 조회
- `GET /projects/{project_id}` - 특정 프로젝트 조회

### 팀 관리
- `POST /teams/` - 새 팀 생성
- `GET /teams/` - 팀 목록 조회
- `GET /teams/{team_id}` - 특정 팀 조회

### 기타
- `GET /statistics` - 전체 통계 조회
- `POST /complex-data/` - 복잡한 데이터 처리

## 🔧 실습 예시

### 1. 을지대학교 학생 등록

```json
{
  "name": "안건",
  "email": "geon0078@g.eulji.ac.kr",
  "student_id": "2022162023",
  "major": "medical_it",
  "grade": 4,
  "role": "student",
  "password": "12345678",
  "confirm_password": "12345678"
}
```

### 2. 을지대학교 을GPT 프로젝트 생성

```json
{
  "name": "을지대학교 을GPT 챗봇",
  "description": "을지대학교 학생들을 위한 AI 기반 질의응답 시스템",
  "category": "ai",
  "team_size": 5,
  "is_active": true
}
```

### 3. 프로젝트 팀 구성

```json
{
  "project_id": 1,
  "members": [
    {
      "student_id": 1,
      "role": "팀장"
    },
    {
      "student_id": 2,
      "role": "개발자"
    }
  ],
  "notes": "을지대학교 을GPT 프로젝트 개발팀"
}
```

## � 새로운 개념

- **Enum 활용**: 을지대학교 전공과 역할을 제한된 값으로 관리
- **중첩 모델**: 프로젝트 팀에 학생 정보 포함
- **커스텀 검증**: 학번 형식과 비밀번호 일치 검증
- **에러 핸들링**: 422 오류에 대한 상세한 정보 제공
- **로깅**: 요청 검증 실패 시 상세 로그 기록

## ⚠️ 주의사항

1. **Enum 값**: API 요청 시 영문 키 사용 (`"medical_it"`, `"student"` 등)
2. **학번 형식**: 숫자만 허용 (8-12자리)
3. **이메일 형식**: 유효한 이메일 형식 필수
4. **비밀번호**: 8자 이상, 확인 비밀번호와 일치 필요

## ✅ 다음 단계

요청 본문 처리를 익혔다면 Step 05로 이동하여 데이터베이스 연동을 학습하세요.
3. 을지대학교 을GPT 새로운 모델과 엔드포인트를 추가해보세요

## 📚 을지대학교 을GPT 새로운 개념

- **을지대학교 을GPT Pydantic 모델**: 을지대학교 학생 데이터 검증을 위한 모델 클래스
- **을지대학교 을GPT 요청 본문**: POST/PUT 요청에 포함된 을지대학교 학생 JSON 데이터
- **을지대학교 을GPT 자동 검증**: FastAPI가 자동으로 수행하는 을지대학교 데이터 검증
- **을지대학교 을GPT 응답 모델**: 을지대학교 을GPT 응답 데이터의 구조 정의

## ✅ 다음 단계

요청 본문 처리를 익혔다면 Step 05로 이동하여 데이터베이스 연결을 학습하세요.
