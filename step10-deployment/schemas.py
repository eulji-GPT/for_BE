"""
을지대학교 을GPT - 배포용 Pydantic 스키마 정의
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 을지대학교 학생 스키마
class EuljiStudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="학생 이름")
    student_number: str = Field(..., min_length=8, max_length=20, description="학번")
    major: str = Field(..., min_length=1, max_length=50, description="전공")
    grade: int = Field(..., ge=1, le=4, description="학년")
    email: EmailStr = Field(..., description="이메일")

class EuljiStudentInDB(EuljiStudentBase):
    """을지대학교 학생 응답용 스키마"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 프로젝트 스키마
class EuljiProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="프로젝트 제목")
    description: Optional[str] = Field(None, max_length=2000, description="프로젝트 설명")
    category: str = Field(..., min_length=1, max_length=100, description="프로젝트 카테고리")
    status: str = Field(default="계획중", description="프로젝트 상태")

class EuljiProjectInDB(EuljiProjectBase):
    """을지대학교 을GPT 프로젝트 응답용 스키마"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# API 응답 스키마
class HealthCheckResponse(BaseModel):
    """헬스체크 응답 스키마"""
    status: str
    university: str
    project: str
    version: str
    environment: str
    timestamp: datetime
    database: str

class SystemStatsResponse(BaseModel):
    """시스템 통계 응답 스키마"""
    university: str
    project: str
    environment: str
    version: str
    statistics: dict
