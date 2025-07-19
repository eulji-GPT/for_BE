"""
을지대학교 을GPT - Step 09: 파일 업로드 시스템
파일 업로드 기능을 구현하고 파일을 안전하게 처리
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path
from PIL import Image
import logging
from datetime import datetime

from database import SessionLocal
from models import EuljiStudent, EuljiProject, FileUpload
from schemas import EuljiStudentInDB, FileUploadResponse

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="을지대학교 을GPT - 파일 업로드 API",
    description="을지대학교 을GPT 프로젝트의 파일 업로드 및 관리 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 파일 업로드 설정
UPLOAD_DIR = Path("uploads")
STUDENT_PROFILES_DIR = UPLOAD_DIR / "student_profiles"
PROJECT_FILES_DIR = UPLOAD_DIR / "project_files"
MEDICAL_IMAGES_DIR = UPLOAD_DIR / "medical_images"

# 디렉토리 생성
for directory in [STUDENT_PROFILES_DIR, PROJECT_FILES_DIR, MEDICAL_IMAGES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# 파일 제한 설정
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024   # 5MB for images
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".md"}
ALLOWED_MEDICAL_EXTENSIONS = {".dcm", ".jpg", ".png", ".tiff"}  # DICOM, 의료 이미지

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 파일 유효성 검사 함수들
def validate_file_size(file: UploadFile, max_size: int = MAX_FILE_SIZE):
    """파일 크기 검사"""
    if file.size > max_size:
        raise HTTPException(
            status_code=413,
            detail=f"파일 크기가 너무 큽니다. 최대 {max_size // 1024 // 1024}MB까지 업로드 가능합니다."
        )

def validate_file_extension(filename: str, allowed_extensions: set):
    """파일 확장자 검사"""
    file_extension = Path(filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"지원하지 않는 파일 형식입니다. 허용된 확장자: {', '.join(allowed_extensions)}"
        )

def generate_unique_filename(original_filename: str) -> str:
    """고유한 파일명 생성"""
    file_extension = Path(original_filename).suffix
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{file_extension}"

def save_uploaded_file(file: UploadFile, directory: Path) -> str:
    """파일을 디스크에 저장"""
    unique_filename = generate_unique_filename(file.filename)
    file_path = directory / unique_filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return unique_filename
    except Exception as e:
        logger.error(f"파일 저장 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="파일 저장에 실패했습니다.")

def resize_image(image_path: Path, max_width: int = 800, max_height: int = 600):
    """이미지 크기 조정"""
    try:
        with Image.open(image_path) as img:
            # 이미지 비율 유지하며 리사이즈
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            img.save(image_path, optimize=True, quality=85)
            logger.info(f"이미지 크기 조정 완료: {image_path}")
    except Exception as e:
        logger.error(f"이미지 크기 조정 실패: {str(e)}")

# 을지대학교 학생 프로필 사진 업로드
@app.post("/students/{student_id}/profile-image", response_model=FileUploadResponse)
async def upload_eulji_student_profile(
    student_id: int,
    file: UploadFile = File(..., description="을지대학교 학생 프로필 이미지"),
    db: Session = Depends(get_db)
):
    """을지대학교 학생 프로필 이미지 업로드"""
    
    # 학생 존재 확인
    student = db.query(EuljiStudent).filter(EuljiStudent.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    
    # 파일 유효성 검사
    validate_file_size(file, MAX_IMAGE_SIZE)
    validate_file_extension(file.filename, ALLOWED_IMAGE_EXTENSIONS)
    
    try:
        # 파일 저장
        saved_filename = save_uploaded_file(file, STUDENT_PROFILES_DIR)
        file_path = STUDENT_PROFILES_DIR / saved_filename
        
        # 이미지 크기 조정 (프로필 사진 최적화)
        resize_image(file_path, max_width=400, max_height=400)
        
        # 데이터베이스에 파일 정보 저장
        file_record = FileUpload(
            filename=saved_filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file.size,
            file_type="profile_image",
            content_type=file.content_type,
            uploaded_by=student_id,
            university="을지대학교",
            project="을GPT"
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        
        logger.info(f"을지대학교 학생 프로필 업로드: {student.name} - {file.filename}")
        
        return FileUploadResponse(
            id=file_record.id,
            filename=saved_filename,
            original_filename=file.filename,
            file_size=file.size,
            content_type=file.content_type,
            upload_url=f"/files/student-profiles/{saved_filename}",
            message="을지대학교 학생 프로필 이미지가 성공적으로 업로드되었습니다."
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"프로필 업로드 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="파일 업로드에 실패했습니다.")

# 을지대학교 을GPT 프로젝트 파일 업로드
@app.post("/projects/{project_id}/files", response_model=FileUploadResponse)
async def upload_eulji_project_file(
    project_id: int,
    file: UploadFile = File(..., description="을지대학교 을GPT 프로젝트 파일"),
    description: Optional[str] = Form(None, description="파일 설명"),
    db: Session = Depends(get_db)
):
    """을지대학교 을GPT 프로젝트 파일 업로드"""
    
    # 프로젝트 존재 확인
    project = db.query(EuljiProject).filter(EuljiProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")
    
    # 파일 유효성 검사
    validate_file_size(file)
    file_extension = Path(file.filename).suffix.lower()
    
    # 파일 유형에 따른 처리
    if file_extension in ALLOWED_IMAGE_EXTENSIONS:
        validate_file_extension(file.filename, ALLOWED_IMAGE_EXTENSIONS)
        file_type = "project_image"
    elif file_extension in ALLOWED_DOCUMENT_EXTENSIONS:
        validate_file_extension(file.filename, ALLOWED_DOCUMENT_EXTENSIONS)
        file_type = "project_document"
    else:
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다."
        )
    
    try:
        # 파일 저장
        saved_filename = save_uploaded_file(file, PROJECT_FILES_DIR)
        file_path = PROJECT_FILES_DIR / saved_filename
        
        # 이미지인 경우 최적화
        if file_type == "project_image":
            resize_image(file_path, max_width=1200, max_height=800)
        
        # 데이터베이스에 파일 정보 저장
        file_record = FileUpload(
            filename=saved_filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file.size,
            file_type=file_type,
            content_type=file.content_type,
            description=description,
            project_id=project_id,
            university="을지대학교",
            project="을GPT"
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        
        logger.info(f"을지대학교 을GPT 프로젝트 파일 업로드: {project.title} - {file.filename}")
        
        return FileUploadResponse(
            id=file_record.id,
            filename=saved_filename,
            original_filename=file.filename,
            file_size=file.size,
            content_type=file.content_type,
            upload_url=f"/files/project-files/{saved_filename}",
            message="을지대학교 을GPT 프로젝트 파일이 성공적으로 업로드되었습니다."
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"프로젝트 파일 업로드 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="파일 업로드에 실패했습니다.")

# 의료 이미지 업로드 (을지대학교 의료IT학과 전용)
@app.post("/medical/images/upload", response_model=FileUploadResponse)
async def upload_medical_image(
    file: UploadFile = File(..., description="의료 이미지 파일"),
    patient_id: Optional[str] = Form(None, description="환자 ID"),
    image_type: str = Form(..., description="이미지 유형 (X-ray, CT, MRI 등)"),
    db: Session = Depends(get_db)
):
    """의료 이미지 업로드 (을지대학교 의료IT학과 전용)"""
    
    # 파일 유효성 검사
    validate_file_size(file)
    validate_file_extension(file.filename, ALLOWED_MEDICAL_EXTENSIONS)
    
    try:
        # 의료 이미지 저장 (환자 정보 보호를 위한 특별한 처리)
        saved_filename = generate_unique_filename(file.filename)
        file_path = MEDICAL_IMAGES_DIR / saved_filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 데이터베이스에 파일 정보 저장
        file_record = FileUpload(
            filename=saved_filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file.size,
            file_type="medical_image",
            content_type=file.content_type,
            description=f"의료 이미지 - {image_type}",
            university="을지대학교",
            project="을GPT_의료",
            metadata={
                "patient_id": patient_id,
                "image_type": image_type,
                "department": "의료IT학과"
            }
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        
        logger.info(f"의료 이미지 업로드: {image_type} - {file.filename}")
        
        return FileUploadResponse(
            id=file_record.id,
            filename=saved_filename,
            original_filename=file.filename,
            file_size=file.size,
            content_type=file.content_type,
            upload_url=f"/files/medical-images/{saved_filename}",
            message="의료 이미지가 성공적으로 업로드되었습니다."
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"의료 이미지 업로드 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="파일 업로드에 실패했습니다.")

# 다중 파일 업로드
@app.post("/files/bulk-upload")
async def bulk_upload_files(
    files: List[UploadFile] = File(..., description="여러 파일 업로드"),
    category: str = Form(..., description="파일 카테고리"),
    db: Session = Depends(get_db)
):
    """다중 파일 업로드"""
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="한 번에 최대 10개의 파일만 업로드 가능합니다.")
    
    uploaded_files = []
    
    for file in files:
        try:
            validate_file_size(file)
            
            # 카테고리에 따른 저장 디렉토리 선택
            if category == "profiles":
                directory = STUDENT_PROFILES_DIR
                validate_file_extension(file.filename, ALLOWED_IMAGE_EXTENSIONS)
            elif category == "projects":
                directory = PROJECT_FILES_DIR
            elif category == "medical":
                directory = MEDICAL_IMAGES_DIR
                validate_file_extension(file.filename, ALLOWED_MEDICAL_EXTENSIONS)
            else:
                directory = UPLOAD_DIR / "general"
                directory.mkdir(exist_ok=True)
            
            saved_filename = save_uploaded_file(file, directory)
            
            uploaded_files.append({
                "original_filename": file.filename,
                "saved_filename": saved_filename,
                "size": file.size,
                "status": "success"
            })
            
        except Exception as e:
            uploaded_files.append({
                "original_filename": file.filename,
                "error": str(e),
                "status": "failed"
            })
    
    return {
        "message": f"{len(files)}개 파일 업로드 처리 완료",
        "results": uploaded_files
    }

# 파일 다운로드 및 조회
@app.get("/files/student-profiles/{filename}")
async def download_student_profile(filename: str):
    """학생 프로필 이미지 다운로드"""
    file_path = STUDENT_PROFILES_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

@app.get("/files/project-files/{filename}")
async def download_project_file(filename: str):
    """프로젝트 파일 다운로드"""
    file_path = PROJECT_FILES_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

@app.get("/files/list")
def list_uploaded_files(
    file_type: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """업로드된 파일 목록 조회"""
    query = db.query(FileUpload)
    
    if file_type:
        query = query.filter(FileUpload.file_type == file_type)
    
    files = query.order_by(FileUpload.uploaded_at.desc()).limit(limit).all()
    
    return {
        "message": "업로드된 파일 목록",
        "count": len(files),
        "files": files
    }

@app.delete("/files/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    """파일 삭제"""
    file_record = db.query(FileUpload).filter(FileUpload.id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    try:
        # 실제 파일 삭제
        file_path = Path(file_record.file_path)
        if file_path.exists():
            file_path.unlink()
        
        # 데이터베이스에서 삭제
        db.delete(file_record)
        db.commit()
        
        logger.info(f"파일 삭제: {file_record.original_filename}")
        return {"message": "파일이 성공적으로 삭제되었습니다."}
        
    except Exception as e:
        db.rollback()
        logger.error(f"파일 삭제 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="파일 삭제에 실패했습니다.")

# 파일 업로드 통계
@app.get("/files/stats")
def get_upload_stats(db: Session = Depends(get_db)):
    """파일 업로드 통계"""
    from sqlalchemy import func
    
    stats = db.query(
        FileUpload.file_type,
        func.count(FileUpload.id).label('count'),
        func.sum(FileUpload.file_size).label('total_size')
    ).group_by(FileUpload.file_type).all()
    
    total_files = db.query(func.count(FileUpload.id)).scalar()
    total_size = db.query(func.sum(FileUpload.file_size)).scalar() or 0
    
    return {
        "total_files": total_files,
        "total_size_mb": round(total_size / 1024 / 1024, 2),
        "by_type": [
            {
                "type": stat.file_type,
                "count": stat.count,
                "size_mb": round((stat.total_size or 0) / 1024 / 1024, 2)
            }
            for stat in stats
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
