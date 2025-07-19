"""
을지대학교 을GPT - SQLAlchemy 모델 정의
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

# 을지대학교 전공 열거형
class EuljiMajor(enum.Enum):
    NURSING = "간호학과"
    RADIOLOGY = "방사선학과"
    MEDICAL_IT = "의료IT학과"

# 프로젝트 상태 열거형
class ProjectStatus(enum.Enum):
    PLANNING = "계획중"
    IN_PROGRESS = "진행중"
    COMPLETED = "완료"
    ON_HOLD = "보류중"

class EuljiStudent(Base):
    """
    을지대학교 학생 모델
    """
    __tablename__ = "eulji_students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    student_number = Column(String(20), unique=True, nullable=False, index=True)
    major = Column(Enum(EuljiMajor), nullable=False, index=True)
    grade = Column(Integer, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계 설정
    projects = relationship("EuljiProject", back_populates="students", secondary="project_members")

class EuljiProject(Base):
    """
    을지대학교 을GPT 프로젝트 모델
    """
    __tablename__ = "eulji_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False, index=True)  # AI프로젝트, 웹개발, 모바일앱, 의료시스템
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING, index=True)
    team_leader_id = Column(Integer, ForeignKey("eulji_students.id"), nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계 설정
    team_leader = relationship("EuljiStudent", foreign_keys=[team_leader_id])
    students = relationship("EuljiStudent", back_populates="projects", secondary="project_members")

# 프로젝트 멤버 연결 테이블
class ProjectMember(Base):
    """
    프로젝트 멤버 연결 테이블
    """
    __tablename__ = "project_members"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("eulji_projects.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("eulji_students.id"), nullable=False)
    role = Column(String(50), default="팀원")  # 팀장, 팀원, 멘토 등
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
