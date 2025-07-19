"""
을지대학교 을GPT - 배포용 데이터베이스 연결 설정
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 환경 변수에서 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv(
    "EULJI_GPT_DATABASE_URL",
    "sqlite:///./eulji_gpt_production.db"  # 기본값으로 SQLite 사용
)

# 프로덕션 환경에서는 PostgreSQL 사용 권장
if os.getenv("EULJI_GPT_ENV") == "production" and DATABASE_URL.startswith("sqlite"):
    print("경고: 프로덕션 환경에서는 PostgreSQL 사용을 권장합니다.")

# SQLite 사용 시 추가 설정
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        echo=False,
        pool_pre_ping=True  # 연결 상태 확인
    )
else:
    engine = create_engine(
        DATABASE_URL, 
        echo=False,
        pool_size=20,  # 프로덕션에서 연결 풀 크기 증가
        max_overflow=0,
        pool_pre_ping=True
    )

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

def create_tables():
    """
    모든 테이블 생성
    """
    from models import EuljiStudent, EuljiProject
    Base.metadata.create_all(bind=engine)
    print("을지대학교 을GPT 배포 데이터베이스 테이블이 생성되었습니다.")

def get_db():
    """
    데이터베이스 세션 의존성 주입용 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 연결 테스트
def test_database_connection():
    """
    데이터베이스 연결 테스트
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"데이터베이스 연결 실패: {str(e)}")
        return False

if __name__ == "__main__":
    create_tables()
    if test_database_connection():
        print("데이터베이스 연결 성공!")
    else:
        print("데이터베이스 연결 실패!")
