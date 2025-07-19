"""
을지대학교 을GPT - 미들웨어용 Pydantic 스키마 정의
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

# 접근 로그 스키마
class AccessLogBase(BaseModel):
    request_id: str = Field(..., description="요청 ID")
    client_ip: str = Field(..., description="클라이언트 IP")
    user_agent: Optional[str] = Field(None, description="User Agent")
    method: str = Field(..., description="HTTP 메서드")
    path: str = Field(..., description="요청 경로")
    status_code: int = Field(..., description="응답 상태 코드")
    response_time: float = Field(..., description="응답 시간(초)")

class AccessLogInDB(AccessLogBase):
    """접근 로그 응답용 스키마"""
    id: int
    timestamp: datetime
    university: str
    project: str
    
    class Config:
        from_attributes = True

# 성능 통계 스키마
class PerformanceStats(BaseModel):
    """성능 통계 스키마"""
    total_requests: int
    average_response_time: float
    slow_requests_count: int
    most_accessed_paths: dict
    
# 미들웨어 응답 스키마
class MiddlewareResponse(BaseModel):
    """미들웨어 응답 스키마"""
    message: str
    university: str = "을지대학교"
    project: str = "을GPT"
    timestamp: datetime
