"""
을지대학교 을GPT - 미들웨어용 데이터베이스 연결 설정
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 환경 변수에서 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv(
    "EULJI_GPT_DATABASE_URL",
    "sqlite:///./eulji_gpt_middleware.db"  # 기본값으로 SQLite 사용
)

# SQLite 사용 시 추가 설정
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        echo=False  # SQL 쿼리 로깅
    )
else:
    engine = create_engine(DATABASE_URL, echo=False)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

def create_tables():
    """
    모든 테이블 생성
    """
    from models import EuljiStudent, AccessLog
    Base.metadata.create_all(bind=engine)
    print("을지대학교 을GPT 미들웨어 데이터베이스 테이블이 생성되었습니다.")

def get_db():
    """
    데이터베이스 세션 의존성 주입용 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
