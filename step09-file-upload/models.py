"""
을지대학교 을GPT - 파일 업로드용 SQLAlchemy 모델 정의
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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

    # 관계 설정
    uploaded_files = relationship("FileUpload", foreign_keys="FileUpload.uploaded_by", back_populates="uploader")

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

    # 관계 설정
    files = relationship("FileUpload", foreign_keys="FileUpload.project_id", back_populates="project")

class FileUpload(Base):
    """
    파일 업로드 모델
    """
    __tablename__ = "file_uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False, index=True)  # 저장된 파일명
    original_filename = Column(String(255), nullable=False)  # 원본 파일명
    file_path = Column(String(500), nullable=False)  # 파일 경로
    file_size = Column(Integer, nullable=False)  # 파일 크기 (bytes)
    file_type = Column(String(50), nullable=False, index=True)  # 파일 유형
    content_type = Column(String(100), nullable=True)  # MIME 타입
    description = Column(Text, nullable=True)  # 파일 설명
    
    # 관계 설정용 외래키
    uploaded_by = Column(Integer, ForeignKey("eulji_students.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("eulji_projects.id"), nullable=True)
    
    # 을지대학교 을GPT 관련 메타데이터
    university = Column(String(50), default="을지대학교")
    project = Column(String(50), default="을GPT")
    metadata = Column(JSON, nullable=True)  # 추가 메타데이터 (JSON 형태)
    
    # 시간 정보
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # 관계 설정
    uploader = relationship("EuljiStudent", foreign_keys=[uploaded_by], back_populates="uploaded_files")
    project_ref = relationship("EuljiProject", foreign_keys=[project_id], back_populates="files")
