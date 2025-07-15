# Step 05: Database Basic - MariaDB 연동

FastAPI와 MariaDB를 연동하여 기본적인 데이터베이스 CRUD 작업을 구현하는 단계입니다.

## 📁 프로젝트 구조

```
step05-database-basic/
├── database.py         # 데이터베이스 연결 및 설정
├── models.py          # SQLAlchemy 모델 정의
├── schemas.py         # Pydantic 스키마 정의
├── create_tables.py   # 테이블 생성 및 샘플 데이터 삽입
├── main.py           # FastAPI 애플리케이션 메인
├── requirements.txt  # 의존성 패키지
├── .env             # 환경변수 설정 (Git 제외)
└── README.md        # 프로젝트 설명
```

## � 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화 (선택사항)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. MariaDB 설정

#### MariaDB 설치 및 실행
1. [MariaDB 공식 사이트](https://mariadb.org/download/)에서 다운로드
2. 설치 과정에서 root 비밀번호 설정
3. MariaDB 서비스 시작 확인

#### 환경변수 설정
`.env` 파일에서 데이터베이스 연결 정보를 설정하세요:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=tutorial_db
ENVIRONMENT=development
```

### 3. 데이터베이스 및 테이블 생성

```bash
# 테이블 생성 및 샘플 데이터 삽입
python create_tables.py
```

이 스크립트는 다음 작업을 수행합니다:
- `users` 테이블 생성 (사용자 정보)
- `posts` 테이블 생성 (게시글 정보)
- 샘플 데이터 삽입 (선택사항)

### 4. FastAPI 애플리케이션 실행

```bash
# 개발 서버 실행
uvicorn main:app --reload

# 서버가 실행되면 다음 URL에서 확인 가능
# http://localhost:8000
# http://localhost:8000/docs (Swagger UI)
```

## 📊 데이터베이스 스키마

### Users 테이블
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | Integer | 기본 키 (자동 증가) |
| username | String(50) | 사용자명 (고유) |
| email | String(100) | 이메일 (고유) |
| full_name | String(100) | 전체 이름 |
| is_active | Boolean | 활성 상태 |
| created_at | DateTime | 생성 시간 |
| updated_at | DateTime | 수정 시간 |

### Posts 테이블
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | Integer | 기본 키 (자동 증가) |
| title | String(200) | 제목 |
| content | Text | 내용 |
| author_id | Integer | 작성자 ID |
| is_published | Boolean | 발행 상태 |
| created_at | DateTime | 생성 시간 |
| updated_at | DateTime | 수정 시간 |

## 🔧 주요 기능

### API 엔드포인트

#### 사용자 관리
- `GET /users/` - 모든 사용자 조회
- `GET /users/{user_id}` - 특정 사용자 조회
- `POST /users/` - 새 사용자 생성
- `PUT /users/{user_id}` - 사용자 정보 수정
- `DELETE /users/{user_id}` - 사용자 삭제

#### 게시글 관리
- `GET /posts/` - 모든 게시글 조회
- `GET /posts/{post_id}` - 특정 게시글 조회
- `POST /posts/` - 새 게시글 생성
- `PUT /posts/{post_id}` - 게시글 수정
- `DELETE /posts/{post_id}` - 게시글 삭제

## 🛠️ 기술 스택

- **FastAPI** - 웹 프레임워크
- **SQLAlchemy** - ORM (Object-Relational Mapping)
- **PyMySQL** - MariaDB/MySQL 드라이버
- **Pydantic** - 데이터 검증 및 직렬화
- **Uvicorn** - ASGI 서버
- **MariaDB** - 관계형 데이터베이스

## 📝 개발 노트

### 데이터베이스 연결 테스트
```bash
# 연결 상태 확인
python database.py
```

### HeidiSQL을 통한 데이터 확인
1. HeidiSQL 실행
2. 연결 정보 입력 (localhost, root, 비밀번호)
3. `tutorial_db` 데이터베이스 선택
4. `users`, `posts` 테이블 데이터 확인

## ⚠️ 주의사항

1. **환경변수**: `.env` 파일은 Git에 커밋하지 마세요
2. **비밀번호**: 실제 운영 환경에서는 강력한 비밀번호 사용
3. **포트**: 기본 포트 3306이 사용 중인지 확인
4. **방화벽**: 필요시 포트 3306 방화벽 설정

## 🔄 다음 단계

- [ ] 인증/권한 시스템 구현
- [ ] 외래 키 관계 설정
- [ ] 데이터 유효성 검사 강화
- [ ] API 테스트 케이스 작성
- [ ] 프론트엔드 연동

## 📚 을지대학교 을GPT 새로운 개념

- **ORM**: Object-Relational Mapping
- **SQLAlchemy**: Python의 SQL 툴킷과 ORM
- **세션**: 데이터베이스와의 연결을 관리하는 객체
- **트랜잭션**: 데이터베이스 작업의 단위

## ✅ 다음 단계

데이터베이스 기초를 익혔다면 Step 06으로 이동하여 CRUD 작업을 학습하세요.
