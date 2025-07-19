"""
을지대학교 을GPT - 배포용 SQLAlchemy 모델 정의
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EuljiStudent(Base):
    """
    을지대학교 학생 모델
    """
    __tablename__ = "eulji_students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    student_number = Column(String(20), unique=True, nullable=False, index=True)
    major = Column(String(50), nullable=False, index=True)
    grade = Column(Integer, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
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
    status = Column(String(50), default="계획중", index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
