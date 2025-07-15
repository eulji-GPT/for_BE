"""
데이터베이스 설정 및 연결 관리 - MariaDB 연동
"""

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# MariaDB 연결 설정
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123")  # 기본값을 123으로 설정
DB_NAME = os.getenv("DB_NAME", "tutorial_db")

# 환경변수 로딩 확인 및 수정
if DB_PASSWORD == "your_password_here":
    print("⚠️  .env 파일 로딩 문제 감지, 기본값 123 사용")
    DB_PASSWORD = "123"

# MariaDB 데이터베이스 URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 연결 상태 확인
    pool_recycle=3600,   # 1시간마다 연결 재생성
    echo=True           # SQL 쿼리 로깅 (개발용)
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성 (모든 모델의 부모 클래스)
Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    """
    데이터베이스 세션을 생성하고 반환하는 의존성 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 초기화 함수
def create_database():
    """
    데이터베이스와 테이블을 생성하는 함수
    """
    Base.metadata.create_all(bind=engine)

# 데이터베이스 연결 테스트 함수
def test_database_connection():
    """
    MariaDB 연결을 테스트하는 함수
    """
    print(f"연결 정보:")
    print(f"- 호스트: {DB_HOST}")
    print(f"- 포트: {DB_PORT}")
    print(f"- 사용자: {DB_USER}")
    print(f"- 데이터베이스: {DB_NAME}")
    print(f"- 연결 URL: mysql+pymysql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    print()
    
    try:
        # 간단한 쿼리로 연결 테스트
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ MariaDB 연결 성공!")
            return True
    except Exception as e:
        print(f"❌ MariaDB 연결 실패: {e}")
        print("\n🔧 해결 방법:")
        print("1. MariaDB 서비스가 실행 중인지 확인")
        print("2. .env 파일의 비밀번호가 정확한지 확인")
        print("3. 아래 명령으로 직접 접속 테스트:")
        print(f"   mysql -u {DB_USER} -p")
        return False

# 데이터베이스 없이 서버 연결만 테스트하는 함수
def test_server_connection():
    """
    데이터베이스 없이 MariaDB 서버 연결만 테스트
    """
    print("📡 MariaDB 서버 연결 테스트 (데이터베이스 없음)...")
    
    # 데이터베이스 없는 연결 URL
    server_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}?charset=utf8mb4"
    
    try:
        test_engine = create_engine(server_url)
        with test_engine.connect() as connection:
            result = connection.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"✅ MariaDB 서버 연결 성공! 버전: {version}")
            
            # 데이터베이스 존재 확인
            result = connection.execute(text(f"SHOW DATABASES LIKE '{DB_NAME}'"))
            if result.fetchone():
                print(f"✅ 데이터베이스 '{DB_NAME}' 존재함")
            else:
                print(f"⚠️  데이터베이스 '{DB_NAME}'가 존재하지 않음")
                print(f"다음 명령으로 생성하세요:")
                print(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            
            return True
    except Exception as e:
        print(f"❌ MariaDB 서버 연결 실패: {e}")
        return False

if __name__ == "__main__":
    # 스크립트 직접 실행시 연결 테스트
    print("🔍 MariaDB 연결 진단을 시작합니다...\n")
    
    # 1단계: 서버 연결 테스트 (데이터베이스 없음)
    if test_server_connection():
        print()
        # 2단계: 데이터베이스 포함 연결 테스트
        test_database_connection()
    
    print("\n" + "="*50)
    print("진단 완료!")
    print("문제가 계속되면 MARIADB_SETUP.md 파일의 트러블슈팅 섹션을 참고하세요.")
