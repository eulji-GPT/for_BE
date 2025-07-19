"""
을지대학교 을GPT - 인증용 SQLAlchemy 모델 정의
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
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
    을지대학교 학생 모델 (인증용)
    """
    __tablename__ = "eulji_students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    student_number = Column(String(20), unique=True, nullable=False, index=True)
    major = Column(Enum(EuljiMajor), nullable=False, index=True)
    grade = Column(Integer, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)  # 해싱된 비밀번호
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class EuljiProject(Base):
    """
    을지대학교 을GPT 프로젝트 모델
    """
    __tablename__ = "eulji_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
