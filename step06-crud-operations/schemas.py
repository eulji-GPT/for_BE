"""
을지대학교 을GPT - Pydantic 스키마 정의
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# 을지대학교 전공 열거형
class EuljiMajor(str, Enum):
    NURSING = "간호학과"
    RADIOLOGY = "방사선학과"
    MEDICAL_IT = "의료IT학과"

# 프로젝트 상태 열거형
class ProjectStatus(str, Enum):
    PLANNING = "계획중"
    IN_PROGRESS = "진행중"
    COMPLETED = "완료"
    ON_HOLD = "보류중"

# 을지대학교 학생 스키마
class EuljiStudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="학생 이름")
    student_number: str = Field(..., min_length=8, max_length=20, description="학번")
    major: EuljiMajor = Field(..., description="전공")
    grade: int = Field(..., ge=1, le=4, description="학년")
    email: EmailStr = Field(..., description="이메일")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")
    address: Optional[str] = Field(None, max_length=500, description="주소")

class EuljiStudentCreate(EuljiStudentBase):
    """을지대학교 학생 생성용 스키마"""
    pass

class EuljiStudentUpdate(BaseModel):
    """을지대학교 학생 수정용 스키마"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    major: Optional[EuljiMajor] = None
    grade: Optional[int] = Field(None, ge=1, le=4)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class EuljiStudentInDB(EuljiStudentBase):
    """을지대학교 학생 응답용 스키마"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 을지대학교 을GPT 프로젝트 스키마
class EuljiProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="프로젝트 제목")
    description: Optional[str] = Field(None, max_length=2000, description="프로젝트 설명")
    category: str = Field(..., min_length=1, max_length=100, description="프로젝트 카테고리")
    team_leader_id: Optional[int] = Field(None, description="팀장 학생 ID")
    start_date: Optional[datetime] = Field(None, description="시작일")
    end_date: Optional[datetime] = Field(None, description="종료일")

class EuljiProjectCreate(EuljiProjectBase):
    """을지대학교 을GPT 프로젝트 생성용 스키마"""
    pass

class EuljiProjectUpdate(BaseModel):
    """을지대학교 을GPT 프로젝트 수정용 스키마"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[ProjectStatus] = None
    team_leader_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class EuljiProjectInDB(EuljiProjectBase):
    """을지대학교 을GPT 프로젝트 응답용 스키마"""
    id: int
    status: ProjectStatus
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 프로젝트 멤버 스키마
class ProjectMemberBase(BaseModel):
    project_id: int = Field(..., description="프로젝트 ID")
    student_id: int = Field(..., description="학생 ID")
    role: str = Field(default="팀원", max_length=50, description="역할")

class ProjectMemberCreate(ProjectMemberBase):
    """프로젝트 멤버 추가용 스키마"""
    pass

class ProjectMemberInDB(ProjectMemberBase):
    """프로젝트 멤버 응답용 스키마"""
    id: int
    joined_at: datetime
    
    class Config:
        from_attributes = True

# 통계용 스키마
class StudentStatsResponse(BaseModel):
    """학생 통계 응답 스키마"""
    total_students: int
    by_major: dict
    by_grade: dict

class ProjectStatsResponse(BaseModel):
    """프로젝트 통계 응답 스키마"""
    total_projects: int
    by_status: dict
    by_category: dict
