"""
을지대학교 을GPT - Step 10: 배포용 FastAPI 애플리케이션
프로덕션 환경에 최적화된 설정
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
import os
import logging
from datetime import datetime

from database import SessionLocal
from models import EuljiStudent, EuljiProject
from schemas import EuljiStudentInDB, EuljiProjectInDB

# 환경 변수에서 설정 가져오기
EULJI_GPT_ENV = os.getenv("EULJI_GPT_ENV", "development")
EULJI_UNIVERSITY = os.getenv("EULJI_UNIVERSITY", "을지대학교")
EULJI_GPT_API_VERSION = os.getenv("EULJI_GPT_API_VERSION", "1.0.0")
EULJI_GPT_SECRET_KEY = os.getenv("EULJI_GPT_SECRET_KEY", "eulji-gpt-development-key")

# 로깅 설정 (환경에 따라 다르게)
if EULJI_GPT_ENV == "production":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('eulji_gpt_production.log'),
            logging.StreamHandler()
        ]
    )
else:
    logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=f"{EULJI_UNIVERSITY} 을GPT - 배포 API",
    description=f"{EULJI_UNIVERSITY} 을GPT 프로젝트 프로덕션 배포용 API",
    version=EULJI_GPT_API_VERSION,
    docs_url="/docs" if EULJI_GPT_ENV != "production" else None,  # 프로덕션에서는 docs 비활성화
    redoc_url="/redoc" if EULJI_GPT_ENV != "production" else None
)

# 프로덕션 환경에서만 TrustedHost 미들웨어 적용
if EULJI_GPT_ENV == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.eulji.ac.kr", "localhost", "127.0.0.1"]
    )

# CORS 설정 (환경에 따라 다르게)
if EULJI_GPT_ENV == "production":
    allowed_origins = [
        "https://eulji.ac.kr",
        "https://gpt.eulji.ac.kr",
        "https://api.eulji.ac.kr"
    ]
else:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 헬스체크 엔드포인트
@app.get("/health")
def health_check():
    """애플리케이션 상태 확인"""
    return {
        "status": "healthy",
        "university": EULJI_UNIVERSITY,
        "project": "을GPT",
        "version": EULJI_GPT_API_VERSION,
        "environment": EULJI_GPT_ENV,
        "timestamp": datetime.now(),
        "database": "connected"  # 실제로는 DB 연결 상태 확인
    }

@app.get("/")
def read_root():
    """을지대학교 을GPT 홈페이지"""
    return {
        "message": f"{EULJI_UNIVERSITY} 을GPT API에 오신 것을 환영합니다!",
        "university": EULJI_UNIVERSITY,
        "project": "을GPT",
        "version": EULJI_GPT_API_VERSION,
        "environment": EULJI_GPT_ENV,
        "status": "running",
        "docs_url": "/docs" if EULJI_GPT_ENV != "production" else "disabled in production"
    }

# 기본 API 엔드포인트들
@app.get("/api/v1/students/", response_model=list[EuljiStudentInDB])
def get_students(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """을지대학교 학생 목록 조회"""
    try:
        students = db.query(EuljiStudent).offset(skip).limit(limit).all()
        logger.info(f"학생 목록 조회: {len(students)}명")
        return students
    except Exception as e:
        logger.error(f"학생 목록 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/students/{student_id}", response_model=EuljiStudentInDB)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """을지대학교 학생 개별 조회"""
    try:
        student = db.query(EuljiStudent).filter(EuljiStudent.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        logger.info(f"학생 조회: {student.name}")
        return student
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"학생 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/projects/", response_model=list[EuljiProjectInDB])
def get_projects(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """을지대학교 을GPT 프로젝트 목록 조회"""
    try:
        projects = db.query(EuljiProject).offset(skip).limit(limit).all()
        logger.info(f"프로젝트 목록 조회: {len(projects)}개")
        return projects
    except Exception as e:
        logger.error(f"프로젝트 목록 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/stats")
def get_system_stats(db: Session = Depends(get_db)):
    """시스템 통계 정보"""
    try:
        from sqlalchemy import func
        
        student_count = db.query(func.count(EuljiStudent.id)).scalar()
        project_count = db.query(func.count(EuljiProject.id)).scalar()
        
        return {
            "university": EULJI_UNIVERSITY,
            "project": "을GPT",
            "environment": EULJI_GPT_ENV,
            "version": EULJI_GPT_API_VERSION,
            "statistics": {
                "total_students": student_count or 0,
                "total_projects": project_count or 0,
                "last_updated": datetime.now()
            }
        }
    except Exception as e:
        logger.error(f"통계 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# 관리자용 엔드포인트 (프로덕션에서는 제한적 접근)
@app.get("/admin/info")
def admin_info():
    """관리자 정보 (개발 환경에서만)"""
    if EULJI_GPT_ENV == "production":
        raise HTTPException(status_code=403, detail="Access denied in production")
    
    return {
        "message": f"{EULJI_UNIVERSITY} 을GPT 관리자 정보",
        "environment_variables": {
            "EULJI_GPT_ENV": EULJI_GPT_ENV,
            "EULJI_UNIVERSITY": EULJI_UNIVERSITY,
            "EULJI_GPT_API_VERSION": EULJI_GPT_API_VERSION,
            "DATABASE_URL": "***" if EULJI_GPT_ENV == "production" else os.getenv("EULJI_GPT_DATABASE_URL", "default")
        }
    }

# 프로덕션 환경에서의 오류 처리
@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return {
        "error": "Internal server error",
        "message": "서버 내부 오류가 발생했습니다." if EULJI_GPT_ENV != "production" else "An error occurred"
    }

# 애플리케이션 시작 시 로깅
@app.on_event("startup")
async def startup_event():
    logger.info(f"{EULJI_UNIVERSITY} 을GPT API 시작됨")
    logger.info(f"Environment: {EULJI_GPT_ENV}")
    logger.info(f"Version: {EULJI_GPT_API_VERSION}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{EULJI_UNIVERSITY} 을GPT API 종료됨")

if __name__ == "__main__":
    import uvicorn
    
    # 환경에 따른 설정
    if EULJI_GPT_ENV == "production":
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            workers=4,  # 프로덕션에서는 여러 워커 사용
            access_log=True,
            log_level="info"
        )
    else:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,  # 개발 환경에서만 리로드
            log_level="debug"
        )
