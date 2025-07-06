# 을지대학교 을GPT - MariaDB 실습 프로젝트

을지대학교 을GPT 프로젝트에서 Python으로 MariaDB를 연결하고 다양한 데이터베이스 작업을 실습하는 예제입니다.

## 📋 목차
1. [환경 설정](#환경-설정)
2. [MariaDB 설치](#mariadb-설치)
3. [Python 패키지 설치](#python-패키지-설치)
4. [실습 파일 설명](#실습-파일-설명)
5. [실행 방법](#실행-방법)
6. [주요 기능](#주요-기능)

## 🔧 환경 설정

### MariaDB 설치

> **권장 버전**: MariaDB 11.4.7 (LTS)

#### Windows
1. [MariaDB 공식 사이트](https://mariadb.org/download/)에서 **MariaDB 11.4.7** 다운로드
   - "Download" 버튼 클릭 → Windows 선택 → MSI Package 다운로드
2. 설치 과정에서 다음 설정을 확인하세요:
   - root 비밀번호 설정 (기억해두세요!)
   - **"Use UTF8 as default server's character set"** 체크박스 선택 ✅
3. 설치 완료 후 서비스 자동 시작됨
4. 설치 확인: `mysql --version`

#### macOS (Homebrew)
```bash
# MariaDB 11.4.7 설치
brew install mariadb@11.4

# 서비스 시작
brew services start mariadb@11.4

# PATH 설정 (필요시)
echo 'export PATH="/opt/homebrew/opt/mariadb@11.4/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Ubuntu/Debian
```bash
# 시스템 업데이트
sudo apt update

# MariaDB 11.4 저장소 추가
sudo apt install software-properties-common
sudo apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'
sudo add-apt-repository 'deb [arch=amd64,arm64,ppc64el] https://mirror.lstn.net/mariadb/repo/11.4/ubuntu focal main'

# MariaDB 11.4 설치
sudo apt update
sudo apt install mariadb-server=1:11.4.7+maria~focal

# 서비스 시작 및 자동 시작 설정
sudo systemctl start mariadb
sudo systemctl enable mariadb

# 보안 설정 (권장)
sudo mysql_secure_installation
```

### MariaDB 초기 설정
```sql
-- MariaDB 접속 (Windows: 시작 메뉴에서 MariaDB Client 실행)
mysql -u root -p

-- 버전 확인
SELECT VERSION();

-- 데이터베이스 생성
CREATE DATABASE test_db;

-- 사용자 생성 (선택사항)
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON test_db.* TO 'testuser'@'localhost';
FLUSH PRIVILEGES;

-- 생성된 데이터베이스 확인
SHOW DATABASES;
```

### 설치 확인
```bash
# 버전 확인
mysql --version

# 서비스 상태 확인 (Linux/macOS)
systemctl status mariadb

# Windows에서 서비스 확인
services.msc에서 MariaDB 서비스 확인
```

## 📦 Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 필요한 패키지
- `PyMySQL`: MariaDB/MySQL 연결용 순수 Python 라이브러리
- `mysql-connector-python`: Oracle 공식 MySQL 커넥터
- `python-dotenv`: 환경 변수 관리

## 📁 실습 파일 설명

### 1. `main.py`
기본적인 MariaDB 연결 및 CRUD 작업을 실습합니다.

**주요 기능:**
- MariaDB 연결 (PyMySQL, mysql-connector-python)
- 테이블 생성
- 데이터 삽입, 조회, 수정, 삭제
- 연결 관리

### 2. `advanced.py`
고급 MariaDB 기능을 실습합니다.

**주요 기능:**
- 외래키 관계 설정
- 복잡한 JOIN 쿼리
- 그룹화 및 집계 함수
- 서브쿼리
- 트랜잭션 처리
- 저장 프로시저

### 3. `.env.example`
환경 변수 설정 예제 파일입니다.

## 🚀 실행 방법

### 1. 환경 변수 설정
```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일에서 MariaDB 연결 정보 수정
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=test_db
```

### 2. 기본 실습 실행
```bash
python main.py
```

### 3. 고급 실습 실행
```bash
python advanced.py
```

## 🎯 주요 기능

### 데이터베이스 연결
- PyMySQL을 사용한 연결
- mysql-connector-python을 사용한 연결
- 연결 풀링 및 관리

### 기본 CRUD 작업
- **CREATE**: 새로운 레코드 생성
- **READ**: 데이터 조회
- **UPDATE**: 기존 데이터 수정
- **DELETE**: 데이터 삭제

### 고급 기능
- **JOIN**: 여러 테이블 조인
- **GROUP BY**: 데이터 그룹화
- **HAVING**: 그룹 조건 필터링
- **서브쿼리**: 중첩 쿼리
- **트랜잭션**: 데이터 일관성 보장
- **저장 프로시저**: 재사용 가능한 SQL 코드

## 📊 데이터베이스 스키마

### users 테이블
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### categories 테이블
```sql
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### products 테이블
```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT,
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

### orders 테이블
```sql
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## 🔍 쿼리 예제

### 기본 조회
```sql
-- 모든 사용자 조회
SELECT * FROM users;

-- 특정 조건으로 조회
SELECT * FROM users WHERE age > 25;
```

### JOIN 쿼리
```sql
-- 사용자별 주문 정보
SELECT u.name, p.name, o.quantity, o.total_price
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN products p ON o.product_id = p.id;
```

### 집계 함수
```sql
-- 카테고리별 상품 수
SELECT c.name, COUNT(p.id) as product_count
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
GROUP BY c.id, c.name;
```

## 🛠️ 트러블슈팅

### 연결 오류
1. MariaDB 서비스가 실행 중인지 확인
2. 포트 번호 확인 (기본: 3306)
3. 사용자 권한 확인
4. 방화벽 설정 확인

### 패키지 설치 오류
```bash
# pip 업그레이드
pip install --upgrade pip

# 패키지 개별 설치
pip install PyMySQL
pip install mysql-connector-python
```

## 📚 참고 자료

- [MariaDB 공식 문서](https://mariadb.org/documentation/)
- [PyMySQL 문서](https://pymysql.readthedocs.io/)
- [MySQL Connector/Python 문서](https://dev.mysql.com/doc/connector-python/en/)
- [Python DB-API 2.0](https://www.python.org/dev/peps/pep-0249/)

## 💡 추가 학습 권장사항

1. **ORM 학습**: SQLAlchemy를 사용한 객체-관계 매핑
2. **연결 풀링**: 대용량 애플리케이션을 위한 연결 관리
3. **보안**: SQL 인젝션 방지 및 안전한 쿼리 작성
4. **성능 최적화**: 인덱스 설계 및 쿼리 최적화
5. **백업 및 복구**: 데이터 보호 전략

---

📝 **참고**: 실제 프로덕션 환경에서는 보안을 위해 환경 변수나 설정 파일을 사용하여 데이터베이스 연결 정보를 관리해야 합니다.
