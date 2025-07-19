# 을지대학교 을GPT - MariaDB 설정 가이드

이 문서는 을지대학교 을GPT 프로젝트를 MariaDB와 연동하는 방법을 설명합니다.

## 📋 사전 준비사항

### 1. MariaDB 서버 설치 및 실행
```bash
# Windows에서 MariaDB 설치
# https://mariadb.org/download/ 에서 설치 파일 다운로드

# 또는 Docker로 MariaDB 실행
docker run -d \
  --name eulji-mariadb \
  -e MYSQL_ROOT_PASSWORD=root_password \
  -e MYSQL_DATABASE=eulji_gpt_db \
  -e MYSQL_USER=eulji_user \
  -e MYSQL_PASSWORD=eulji_password \
  -p 3306:3306 \
  mariadb:latest
```

### 2. MariaDB 데이터베이스 및 사용자 생성
```sql
-- MariaDB 콘솔에 root로 접속 후 실행
CREATE DATABASE eulji_gpt_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 을지대학교 을GPT 전용 사용자 생성
CREATE USER 'eulji_user'@'localhost' IDENTIFIED BY 'eulji_password';
CREATE USER 'eulji_user'@'%' IDENTIFIED BY 'eulji_password';

-- 권한 부여
GRANT ALL PRIVILEGES ON eulji_gpt_db.* TO 'eulji_user'@'localhost';
GRANT ALL PRIVILEGES ON eulji_gpt_db.* TO 'eulji_user'@'%';

-- 권한 적용
FLUSH PRIVILEGES;

-- 생성 확인
SHOW DATABASES;
SELECT User, Host FROM mysql.user WHERE User = 'eulji_user';
```

## 🔧 프로젝트 설정

### 1. 환경 설정 파일 생성
```bash
# .env.example을 .env로 복사
copy .env.example .env

# .env 파일에서 MariaDB 연결 정보 수정
MARIADB_HOST=localhost
MARIADB_PORT=3306
MARIADB_DATABASE=eulji_gpt_db
MARIADB_USERNAME=eulji_user
MARIADB_PASSWORD=eulji_password
```

### 2. Python 패키지 설치
```bash
# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 패키지 설치 (MariaDB 연동 포함)
pip install -r requirements.txt
```

### 3. MariaDB 연결 테스트 및 초기 설정
```bash
# MariaDB 연결 테스트 및 테이블 생성
python database.py

# 샘플 데이터 생성 (선택사항)
python setup_mariadb.py
```

## 🚀 애플리케이션 실행

```bash
# FastAPI 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# API 문서 확인
# http://localhost:8000/docs
```

## 📊 생성되는 테이블 구조

### 1. eulji_students (을지대학교 학생)
- id (INT, PK)
- name (VARCHAR(100)) - 학생 이름
- student_number (VARCHAR(20), UNIQUE) - 학번
- major (ENUM) - 전공 (간호학과, 방사선학과, 의료IT학과)
- grade (INT) - 학년 (1-4)
- email (VARCHAR(255), UNIQUE) - 이메일
- phone (VARCHAR(20)) - 전화번호
- address (TEXT) - 주소
- is_active (BOOLEAN) - 활성 상태
- created_at (DATETIME) - 생성일시
- updated_at (DATETIME) - 수정일시

### 2. eulji_projects (을지대학교 을GPT 프로젝트)
- id (INT, PK)
- title (VARCHAR(200)) - 프로젝트 제목
- description (TEXT) - 프로젝트 설명
- category (VARCHAR(100)) - 카테고리 (AI프로젝트, 웹개발, 모바일앱, 의료시스템)
- status (ENUM) - 상태 (계획중, 진행중, 완료, 보류중)
- team_leader_id (INT, FK) - 팀장 학생 ID
- start_date (DATETIME) - 시작일
- end_date (DATETIME) - 종료일
- is_active (BOOLEAN) - 활성 상태
- created_at (DATETIME) - 생성일시
- updated_at (DATETIME) - 수정일시

### 3. project_members (프로젝트 멤버 관계)
- id (INT, PK)
- project_id (INT, FK) - 프로젝트 ID
- student_id (INT, FK) - 학생 ID
- role (VARCHAR(50)) - 역할 (팀장, 팀원, 멘토 등)
- joined_at (DATETIME) - 참여일시

## 🔍 샘플 데이터

### 을지대학교 학생 (5명)
1. **김간호** (간호학과 3학년) - nursing01@eulji.ac.kr
2. **박방사** (방사선학과 4학년) - radiology01@eulji.ac.kr
3. **이의료** (의료IT학과 2학년) - medicalit01@eulji.ac.kr
4. **정을지** (간호학과 1학년) - nursing02@eulji.ac.kr
5. **최GPT** (의료IT학과 4학년) - medicalit02@eulji.ac.kr

### 을지대학교 을GPT 프로젝트 (4개)
1. **AI 진단 지원 시스템** - AI프로젝트 (진행중)
2. **환자 관리 웹 플랫폼** - 웹개발 (계획중)
3. **간호 교육 모바일 앱** - 모바일앱 (완료)
4. **의료기기 IoT 모니터링** - 의료시스템 (진행중)

## 🛠️ API 엔드포인트

### 학생 관리
- `GET /students/` - 학생 목록 (필터링, 페이지네이션)
- `POST /students/` - 새 학생 생성
- `GET /students/{student_id}` - 특정 학생 조회
- `PUT /students/{student_id}` - 학생 정보 수정
- `DELETE /students/{student_id}` - 학생 삭제
- `GET /students/major/{major}` - 전공별 학생 조회

### 프로젝트 관리
- `GET /projects/` - 프로젝트 목록
- `POST /projects/` - 새 프로젝트 생성
- `PUT /projects/{project_id}` - 프로젝트 수정
- `GET /projects/status/{status}` - 상태별 프로젝트 조회

### 통계
- `GET /stats/students-by-major` - 전공별 학생 통계
- `GET /stats/projects-by-status` - 상태별 프로젝트 통계

## ❗ 문제해결

### MariaDB 연결 실패 시
1. **서비스 확인**: MariaDB 서비스가 실행 중인지 확인
2. **포트 확인**: 3306 포트가 사용 가능한지 확인
3. **방화벽 확인**: 방화벽에서 3306 포트 허용
4. **인증 정보 확인**: username, password, database 이름 확인

### 한글 깨짐 현상
```sql
-- 데이터베이스 문자셋 확인
SHOW VARIABLES LIKE 'character_set%';

-- utf8mb4로 설정 확인
ALTER DATABASE eulji_gpt_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 패키지 설치 오류
```bash
# MySQL 클라이언트 라이브러리가 필요한 경우
# Windows: Microsoft Visual C++ Build Tools 설치 후
pip install pymysql

# 또는 바이너리 패키지 사용
pip install pymysql cryptography
```

## 📞 지원

을지대학교 을GPT 프로젝트 MariaDB 연동 관련 문의사항이 있으시면 언제든지 연락 주세요.

---
**을지대학교 을GPT 프로젝트** - MariaDB 기반 의료 교육 데이터 관리 시스템
