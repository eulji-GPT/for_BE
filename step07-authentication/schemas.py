"""
을지대학교 을GPT - 인증용 Pydantic 스키마 정의
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# 을지대학교 전공 열거형
class EuljiMajor(str, Enum):
    NURSING = "간호학과"
    RADIOLOGY = "방사선학과"
    MEDICAL_IT = "의료IT학과"

# 인증 관련 스키마
class EuljiStudentLogin(BaseModel):
    """을지대학교 학생 로그인용 스키마"""
    student_number: str = Field(..., min_length=8, max_length=20, description="학번")
    password: str = Field(..., min_length=8, description="비밀번호")

class Token(BaseModel):
    """JWT 토큰 응답 스키마"""
    access_token: str
    token_type: str
    expires_in: int
    student_info: dict

class TokenData(BaseModel):
    """토큰 데이터 스키마"""
    student_number: Optional[str] = None

# 을지대학교 학생 스키마
class EuljiStudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="학생 이름")
    student_number: str = Field(..., min_length=8, max_length=20, description="학번")
    major: EuljiMajor = Field(..., description="전공")
    grade: int = Field(..., ge=1, le=4, description="학년")
    email: EmailStr = Field(..., description="이메일")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")

class EuljiStudentCreate(EuljiStudentBase):
    """을지대학교 학생 회원가입용 스키마"""
    password: str = Field(..., min_length=8, description="비밀번호")

class EuljiStudentInDB(EuljiStudentBase):
    """을지대학교 학생 응답용 스키마"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 비밀번호 변경 스키마
class PasswordChange(BaseModel):
    """비밀번호 변경용 스키마"""
    old_password: str = Field(..., min_length=8, description="현재 비밀번호")
    new_password: str = Field(..., min_length=8, description="새 비밀번호")
