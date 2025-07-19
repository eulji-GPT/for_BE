# 을지대학교 을GPT 프로젝트 - Backend 실습 파일 (MariaDB 연동)

이 프로젝트는 을지대학교 을GPT 프로젝트의 백엔드 개발을 위한 실습 파일들입니다. **실제 MariaDB 데이터베이스와 연동되어 운영 환경과 유사한 경험을 제공합니다.**

## 🗄️ 데이터베이스 환경

### MariaDB 연동의 장점
- **고성능**: SQLite보다 뛰어난 성능과 동시성 처리
- **확장성**: 대량의 데이터와 다중 사용자 지원  
- **안정성**: 트랜잭션 관리 및 데이터 무결성 보장
- **실무 적용성**: 실제 운영 환경에서 널리 사용되는 데이터베이스

### 빠른 MariaDB 환경 구성
```bash
# Docker로 MariaDB 환경 시작
start_mariadb.bat

# 또는 수동 실행
docker-compose -f docker-compose.mariadb.yml up -d

# phpMyAdmin 접속: http://localhost:8080
# MariaDB 포트: 3306
```

## 📋 프로젝트 구성

### Step 06: CRUD 작업 (★ MariaDB 연동)
- **파일**: `step06-crud-operations/`
- **데이터베이스**: MariaDB 기반 CRUD 작업
- **주요 기능**:
  - 을지대학교 학생 관리 (간호학과, 방사선학과, 의료IT학과)
  - 을GPT 프로젝트 관리 (AI프로젝트, 웹개발, 모바일앱, 의료시스템)
  - **MariaDB 트랜잭션 관리 및 무결성 보장**
  - **인덱스 활용한 고성능 검색**
  - 전공별, 학년별 필터링 및 통계
  - **관계형 데이터베이스 특성을 활용한 JOIN 쿼리**

### Step 07: 인증 시스템 (MariaDB 호환)
- **파일**: `step07-authentication/`
- **내용**: JWT 토큰 기반 을지대학교 학생 인증 시스템
- **주요 기능**:
  - 을지대학교 학번 기반 회원가입/로그인
  - **MariaDB에 안전한 비밀번호 해시 저장**
  - JWT 토큰 생성 및 검증
  - 전공별, 학년별 권한 관리
  - **데이터베이스 세션 관리 및 보안**

### Step 08: 미들웨어 (MariaDB 로깅)
- **파일**: `step08-middleware/`
- **내용**: FastAPI 미들웨어를 활용한 요청/응답 처리
- **주요 기능**:
  - 을지대학교 을GPT 커스텀 로깅 미들웨어
  - **MariaDB 기반 접근 로그 저장**
  - 보안 헤더 추가 및 접근 제한
  - 성능 모니터링 및 통계
  - CORS, GZip, TrustedHost 미들웨어

### Step 09: 파일 업로드 (MariaDB 메타데이터)
- **파일**: `step09-file-upload/`
- **내용**: 안전하고 효율적인 파일 업로드 시스템
- **주요 기능**:
  - 을지대학교 학생 프로필 사진 업로드
  - 을GPT 프로젝트 파일 관리
  - **MariaDB에 파일 메타데이터 저장**
  - 의료 이미지 업로드 (의료IT학과 전용)
  - **관계형 DB를 활용한 파일-사용자 관계 관리**

### Step 10: 배포 (MariaDB 프로덕션)
- **파일**: `step10-deployment/`
- **내용**: 프로덕션 환경 배포를 위한 설정
- **주요 기능**:
  - **MariaDB 프로덕션 환경 설정**
  - Docker 컨테이너화
  - 환경변수 관리 및 보안 설정
  - **데이터베이스 연결 풀링 최적화**
  - 헬스체크 및 모니터링

## 🚀 실행 방법

### 1. MariaDB 환경 구성 (필수)
```bash
# Docker로 MariaDB 환경 시작
start_mariadb.bat

# 연결 정보 확인
# 호스트: localhost:3306
# 데이터베이스: eulji_gpt_db  
# 사용자: eulji_user / eulji_password
# phpMyAdmin: http://localhost:8080
```

### 2. 각 단계별 실행
```bash
# Step 06으로 이동
cd step06-crud-operations

# 환경 설정 복사 및 수정
copy .env.example .env

# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# MariaDB 연동 패키지 설치
pip install -r requirements.txt

# MariaDB 연결 테스트 및 테이블 생성
python database.py

# 샘플 데이터 생성 (선택사항)
python setup_mariadb.py

# 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 모든 서비스 한번에 실행
```bash
# 모든 서비스 실행 (각각 다른 포트)
start_all_services.bat

# API 테스트
python test_all_apis.py
```

## 🛠️ 기술 스택

### Backend Framework
- **FastAPI** 0.104.1 - 현대적이고 빠른 API 프레임워크
- **Uvicorn** - ASGI 서버
- **Pydantic** 2.5.0 - 데이터 검증 및 시리얼라이제이션

### Database & ORM
- **MariaDB** 10.11 - 고성능 오픈소스 관계형 데이터베이스
- **SQLAlchemy** 2.0.23 - Python SQL 툴킷 및 ORM
- **PyMySQL** 1.1.0 - MariaDB/MySQL 연동 드라이버

### Authentication & Security
- **JWT** (python-jose) - 토큰 기반 인증
- **bcrypt** (passlib) - 비밀번호 해싱
- **cryptography** - 암호화 라이브러리

### File Processing
- **Pillow** 10.1.0 - 이미지 처리 라이브러리

### DevOps & Deployment
- **Docker & Docker Compose** - 컨테이너화
- **Gunicorn** - 프로덕션 WSGI 서버

## 📊 MariaDB 데이터베이스 스키마

### 주요 테이블 구조

#### 1. eulji_students (을지대학교 학생)
```sql
CREATE TABLE eulji_students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    student_number VARCHAR(20) UNIQUE NOT NULL,
    major ENUM('간호학과', '방사선학과', '의료IT학과') NOT NULL,
    grade INT NOT NULL CHECK (grade BETWEEN 1 AND 4),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_major_grade (major, grade),
    INDEX idx_student_number (student_number),
    INDEX idx_email (email)
);
```

#### 2. eulji_projects (을GPT 프로젝트)
```sql
CREATE TABLE eulji_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    status ENUM('계획중', '진행중', '완료', '보류중') DEFAULT '계획중',
    team_leader_id INT,
    start_date DATETIME,
    end_date DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (team_leader_id) REFERENCES eulji_students(id),
    INDEX idx_status_category (status, category),
    INDEX idx_team_leader (team_leader_id)
);
```

#### 3. project_members (프로젝트 멤버 관계)
```sql
CREATE TABLE project_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    student_id INT NOT NULL,
    role VARCHAR(50) DEFAULT '팀원',
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES eulji_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES eulji_students(id) ON DELETE CASCADE,
    UNIQUE KEY unique_project_student (project_id, student_id)
);
```

### 샘플 데이터
- **을지대학교 학생**: 5명 (각 전공별 샘플)
- **을GPT 프로젝트**: 4개 (AI, 웹, 모바일, 의료시스템)
- **프로젝트 멤버 관계**: 8개 관계

## 🔐 보안 기능

- **JWT 토큰 기반 인증** - stateless 인증 시스템
- **비밀번호 bcrypt 해싱** - MariaDB에 안전한 해시 저장
- **전공별/학년별 권한 관리** - 세밀한 접근 제어
- **파일 업로드 보안 검증** - MIME 타입 및 크기 제한
- **SQL 인젝션 방지** - SQLAlchemy ORM 사용
- **CORS 및 보안 헤더** - XSS, CSRF 방지

## 🏥 을지대학교 특화 기능

- **을지대학교 3개 전공** 완벽 지원 (간호학과, 방사선학과, 의료IT학과)
- **을GPT 프로젝트 카테고리** 관리 (AI프로젝트, 웹개발, 모바일앱, 의료시스템)
- **의료 이미지 전용 업로드** - DICOM 파일 지원
- **을지대학교 브랜딩** - 모든 API 응답에 대학교 정보 포함
- **한글 완벽 지원** - utf8mb4 문자셋으로 한글 데이터 처리

## 📝 API 문서

각 서비스 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- **Step06 CRUD**: http://localhost:8000/docs
- **Step07 인증**: http://localhost:8001/docs  
- **Step08 미들웨어**: http://localhost:8002/docs
- **Step09 파일업로드**: http://localhost:8003/docs
- **Step10 배포**: http://localhost:8004/docs

## 🐳 Docker 환경

### MariaDB 컨테이너
```bash
# MariaDB + phpMyAdmin 실행
docker-compose -f docker-compose.mariadb.yml up -d

# 컨테이너 상태 확인  
docker-compose -f docker-compose.mariadb.yml ps

# 로그 확인
docker-compose -f docker-compose.mariadb.yml logs
```

### 접속 정보
- **MariaDB**: localhost:3306
- **phpMyAdmin**: http://localhost:8080
  - 사용자: root / eulji_root_2024
  - 또는: eulji_user / eulji_password

## 📈 성능 최적화

### 데이터베이스 최적화
- **인덱스 설계**: 자주 조회되는 컬럼에 복합 인덱스 적용
- **쿼리 최적화**: EXPLAIN을 활용한 실행 계획 분석
- **연결 풀링**: SQLAlchemy 연결 풀을 통한 효율적인 DB 연결 관리
- **트랜잭션 관리**: ACID 특성을 활용한 데이터 무결성 보장

### 애플리케이션 최적화
- **비동기 처리**: FastAPI의 async/await 활용
- **캐싱**: 자주 조회되는 데이터 캐싱 전략
- **페이지네이션**: 대량 데이터 조회 시 메모리 효율성

## 📚 문서 및 가이드

- **[MARIADB_SETUP.md](step06-crud-operations/MARIADB_SETUP.md)** - 상세 MariaDB 설정 가이드
- **[FastAPI Documentation](https://fastapi.tiangolo.com/)**
- **[SQLAlchemy Documentation](https://docs.sqlalchemy.org/)**
- **[MariaDB Documentation](https://mariadb.com/kb/)**

## ❗ 문제해결

### MariaDB 연결 실패
1. Docker Desktop이 실행 중인지 확인
2. 포트 3306이 사용 중인지 확인 (`netstat -an | grep 3306`)
3. 방화벽에서 3306 포트 허용 확인
4. `.env` 파일의 연결 정보 확인

### 한글 데이터 깨짐
```sql
-- MariaDB에서 문자셋 확인
SHOW VARIABLES LIKE 'character_set%';
-- utf8mb4 설정 확인 후 애플리케이션 재시작
```

## 📞 지원

을지대학교 을GPT 프로젝트 관련 문의사항이 있으시면 언제든지 연락 주세요.

---
**을지대학교 을GPT 프로젝트** - MariaDB 기반 혁신적인 의료 교육 AI 백엔드 시스템

## 🚀 실행 방법

### 1. 모든 서비스 한번에 실행
```bash
# Windows
start_all_services.bat

# 각 서비스가 다음 포트에서 실행됩니다:
# Step06: http://localhost:8000
# Step07: http://localhost:8001
# Step08: http://localhost:8002
# Step09: http://localhost:8003
# Step10: http://localhost:8004
```

### 2. 개별 서비스 실행
```bash
# 원하는 단계로 이동
cd step06-crud-operations

# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 데이터베이스 테이블 생성
python database.py

# 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. API 테스트
```bash
# 모든 API 테스트 실행
python test_all_apis.py
```

## 🛠️ 기술 스택

- **Framework**: FastAPI 0.104.1
- **Database**: SQLAlchemy 2.0.23 + SQLite (개발용)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Image Processing**: Pillow
- **Validation**: Pydantic 2.5.0
- **Server**: Uvicorn
- **Containerization**: Docker & Docker Compose

## 📊 데이터베이스 스키마

### EuljiStudent (을지대학교 학생)
- id, name, student_number, major, grade, email
- 전공: 간호학과, 방사선학과, 의료IT학과

### EuljiProject (을GPT 프로젝트)  
- id, title, description, category, status
- 카테고리: AI프로젝트, 웹개발, 모바일앱, 의료시스템

### FileUpload (파일 업로드)
- 프로필 사진, 프로젝트 파일, 의료 이미지 관리

## 🔐 보안 기능

- JWT 토큰 기반 인증
- 비밀번호 bcrypt 해싱
- 전공별/학년별 권한 관리
- 파일 업로드 보안 검증
- CORS 및 보안 헤더 설정

## 🏥 을지대학교 특화 기능

- 을지대학교 3개 전공 (간호학과, 방사선학과, 의료IT학과) 지원
- 을GPT 프로젝트 카테고리 관리
- 의료 이미지 전용 업로드 시스템
- 을지대학교 브랜딩 적용

## 📝 API 문서

각 서비스 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Step06: http://localhost:8000/docs
- Step07: http://localhost:8001/docs
- Step08: http://localhost:8002/docs
- Step09: http://localhost:8003/docs
- Step10: http://localhost:8004/docs

## 🐳 Docker 실행

```bash
cd step10-deployment

# Docker Compose로 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

## 📞 문의사항

을지대학교 을GPT 프로젝트 관련 문의사항이 있으시면 언제든지 연락 주세요.

---
**을지대학교 을GPT 프로젝트** - 혁신적인 의료 교육을 위한 AI 기반 백엔드 시스템
