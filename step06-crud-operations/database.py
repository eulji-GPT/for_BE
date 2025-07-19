"""
을지대학교 을GPT - MariaDB 데이터베이스 연결 설정
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# MariaDB 연결 설정
MARIADB_CONFIG = {
    "host": os.getenv("MARIADB_HOST", "localhost"),
    "port": os.getenv("MARIADB_PORT", "3306"),
    "database": os.getenv("MARIADB_DATABASE", "eulji_gpt_db"),
    "username": os.getenv("MARIADB_USERNAME", "eulji_user"),
    "password": os.getenv("MARIADB_PASSWORD", "eulji_password")
}

# MariaDB URL 생성
DATABASE_URL = os.getenv(
    "EULJI_GPT_DATABASE_URL",
    f"mysql+pymysql://{MARIADB_CONFIG['username']}:{MARIADB_CONFIG['password']}@"
    f"{MARIADB_CONFIG['host']}:{MARIADB_CONFIG['port']}/{MARIADB_CONFIG['database']}"
    f"?charset=utf8mb4"
)

# MariaDB 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=False,  # SQL 쿼리 로깅 (개발시에는 True로 설정)
    pool_size=10,  # 연결 풀 크기
    max_overflow=20,  # 최대 오버플로우 연결 수
    pool_timeout=30,  # 연결 타임아웃 (초)
    pool_recycle=3600,  # 연결 재활용 시간 (1시간)
    pool_pre_ping=True  # 연결 상태 확인
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

def create_tables():
    """
    MariaDB에 모든 테이블 생성
    """
    from models import EuljiStudent, EuljiProject, ProjectMember
    Base.metadata.create_all(bind=engine)
    print("을지대학교 을GPT MariaDB 데이터베이스 테이블이 생성되었습니다.")
    print(f"연결된 데이터베이스: {MARIADB_CONFIG['database']}")
    print(f"호스트: {MARIADB_CONFIG['host']}:{MARIADB_CONFIG['port']}")

def get_db():
    """
    MariaDB 세션 의존성 주입용 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_mariadb_connection():
    """
    MariaDB 연결 테스트
    """
    try:
        db = SessionLocal()
        result = db.execute("SELECT 1 as test").fetchone()
        db.close()
        if result:
            print("✅ MariaDB 연결 성공!")
            print(f"테스트 결과: {result[0]}")
            return True
    except Exception as e:
        print(f"❌ MariaDB 연결 실패: {str(e)}")
        print("MariaDB 서버가 실행 중인지, 연결 정보가 올바른지 확인해주세요.")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("을지대학교 을GPT MariaDB 설정")
    print("=" * 50)
    print(f"데이터베이스: {MARIADB_CONFIG['database']}")
    print(f"호스트: {MARIADB_CONFIG['host']}:{MARIADB_CONFIG['port']}")
    print(f"사용자: {MARIADB_CONFIG['username']}")
    print("=" * 50)
    
    if test_mariadb_connection():
        create_tables()
    else:
        print("\n⚠️  MariaDB 연결에 실패했습니다.")
        print("다음 사항을 확인해주세요:")
        print("1. MariaDB 서버가 실행 중인지 확인")
        print("2. 데이터베이스가 존재하는지 확인")
        print("3. 사용자 권한이 올바른지 확인")
        print("4. 환경 변수 설정이 올바른지 확인")
