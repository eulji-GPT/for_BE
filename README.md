# FastAPI 백엔드 튜토리얼

이 프로젝트는 FastAPI를 사용한 백엔드 개발을 단계별로 학습할 수 있도록 구성된 교육용 튜토리얼입니다.

## 📚 튜토리얼 구성

### Step 01: 기본 설정 (step01-basic-setup)
- FastAPI 설치 및 환경 설정
- 기본 프로젝트 구조 생성
- 가상환경 설정

### Step 02: 첫 번째 API (step02-first-api)
- 간단한 Hello World API 생성
- FastAPI 서버 실행
- 자동 생성되는 API 문서 확인

### Step 03: 경로 매개변수 (step03-path-parameters)
- 동적 경로 처리
- 경로 매개변수 유효성 검사
- 여러 매개변수 처리

### Step 04: 요청 본문 (step04-request-body)
- POST 요청 처리
- Pydantic 모델 사용
- 요청 데이터 검증

### Step 05: 데이터베이스 기초 (step05-database-basic)
- SQLite 연결 설정
- 기본 테이블 생성
- 데이터베이스 연결 관리

### Step 06: CRUD 작업 (step06-crud-operations)
- Create, Read, Update, Delete 구현
- 데이터베이스 쿼리 작성
- 에러 처리

### Step 07: 인증 (step07-authentication)
- JWT 토큰 기반 인증
- 사용자 로그인/회원가입
- 보안 미들웨어

### Step 08: 미들웨어 (step08-middleware)
- 커스텀 미들웨어 작성
- CORS 설정
- 로깅 미들웨어

### Step 09: 파일 업로드 (step09-file-upload)
- 파일 업로드 처리
- 이미지 파일 검증
- 파일 저장 및 관리

### Step 10: 배포 (step10-deployment)
- Docker 컨테이너화
- 환경 변수 설정
- 프로덕션 배포 준비

## 🚀 시작하기

각 단계의 폴더에 들어가서 해당 단계의 README.md 파일을 확인하고 순서대로 따라하세요.

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

## 📋 요구사항

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

## 📝 학습 순서

1. 각 단계를 순서대로 진행하세요
2. 각 단계의 코드를 직접 작성해보세요
3. API 문서를 확인하며 테스트해보세요
4. 다음 단계로 넘어가기 전에 완전히 이해했는지 확인하세요
