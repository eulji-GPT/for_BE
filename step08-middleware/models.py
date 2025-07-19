"""
을지대학교 을GPT - 미들웨어용 SQLAlchemy 모델 정의
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

# 을지대학교 전공 열거형
class EuljiMajor(enum.Enum):
    NURSING = "간호학과"
    RADIOLOGY = "방사선학과"
    MEDICAL_IT = "의료IT학과"

class EuljiStudent(Base):
    """
    을지대학교 학생 모델
    """
    __tablename__ = "eulji_students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    student_number = Column(String(20), unique=True, nullable=False, index=True)
    major = Column(String(50), nullable=False, index=True)  # 간단히 문자열로 처리
    grade = Column(Integer, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AccessLog(Base):
    """
    을지대학교 을GPT 접근 로그 모델
    """
    __tablename__ = "access_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(36), nullable=False, index=True)  # UUID
    client_ip = Column(String(45), nullable=False, index=True)  # IPv6 지원
    user_agent = Column(Text, nullable=True)
    method = Column(String(10), nullable=False)
    path = Column(String(500), nullable=False, index=True)
    status_code = Column(Integer, nullable=False)
    response_time = Column(Float, nullable=False)  # 초 단위
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # 을지대학교 을GPT 관련 추가 필드
    university = Column(String(50), default="을지대학교")
    project = Column(String(50), default="을GPT")
