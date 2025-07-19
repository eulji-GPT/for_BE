"""
을지대학교 을GPT - 파일 업로드용 Pydantic 스키마 정의
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
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

# 파일 업로드 스키마
class FileUploadBase(BaseModel):
    filename: str = Field(..., description="저장된 파일명")
    original_filename: str = Field(..., description="원본 파일명")
    file_size: int = Field(..., description="파일 크기 (bytes)")
    file_type: str = Field(..., description="파일 유형")
    content_type: Optional[str] = Field(None, description="MIME 타입")
    description: Optional[str] = Field(None, description="파일 설명")

class FileUploadResponse(BaseModel):
    """파일 업로드 응답 스키마"""
    id: int
    filename: str
    original_filename: str
    file_size: int
    content_type: Optional[str]
    upload_url: str
    message: str

class FileUploadInDB(FileUploadBase):
    """파일 업로드 DB 응답용 스키마"""
    id: int
    file_path: str
    uploaded_by: Optional[int]
    project_id: Optional[int]
    university: str
    project: str
    metadata: Optional[Dict[str, Any]]
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# 프로젝트 스키마
class EuljiProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="프로젝트 제목")
    description: Optional[str] = Field(None, max_length=2000, description="프로젝트 설명")
    category: str = Field(..., min_length=1, max_length=100, description="프로젝트 카테고리")

class EuljiProjectInDB(EuljiProjectBase):
    """을지대학교 을GPT 프로젝트 응답용 스키마"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 파일 업로드 통계 스키마
class FileUploadStats(BaseModel):
    """파일 업로드 통계 스키마"""
    total_files: int
    total_size_mb: float
    by_type: list

class BulkUploadResponse(BaseModel):
    """다중 파일 업로드 응답 스키마"""
    message: str
    results: list

# 의료 이미지 업로드 스키마
class MedicalImageUpload(BaseModel):
    """의료 이미지 업로드 요청 스키마"""
    patient_id: Optional[str] = Field(None, description="환자 ID")
    image_type: str = Field(..., description="이미지 유형")
    description: Optional[str] = Field(None, description="이미지 설명")
