"""
을지대학교 을GPT - Step 08: 미들웨어 시스템
FastAPI 미들웨어를 사용하여 요청/응답 처리를 커스터마이징
"""

from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.orm import Session
import time
import logging
import json
import uuid
from datetime import datetime
from typing import Callable

from database import SessionLocal
from models import EuljiStudent, AccessLog
from schemas import EuljiStudentInDB

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('eulji_gpt_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="을지대학교 을GPT - 미들웨어 API",
    description="을지대학교 을GPT 프로젝트의 커스텀 미들웨어 시스템",
    version="1.0.0"
)

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. 을지대학교 을GPT 커스텀 로깅 미들웨어
@app.middleware("http")
async def eulji_gpt_logging_middleware(request: Request, call_next: Callable):
    """
    을지대학교 을GPT 요청/응답 로깅 미들웨어
    """
    # 요청 시작 시간
    start_time = time.time()
    
    # 요청 ID 생성
    request_id = str(uuid.uuid4())
    
    # 클라이언트 정보
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    # 요청 로깅
    logger.info(
        f"을지대학교 을GPT 요청 시작 - "
        f"ID: {request_id} | "
        f"Method: {request.method} | "
        f"URL: {request.url} | "
        f"Client: {client_ip} | "
        f"User-Agent: {user_agent}"
    )
    
    # 요청 처리
    try:
        response = await call_next(request)
        
        # 처리 시간 계산
        process_time = time.time() - start_time
        
        # 응답 로깅
        logger.info(
            f"을지대학교 을GPT 요청 완료 - "
            f"ID: {request_id} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time:.4f}s"
        )
        
        # 응답 헤더에 처리 시간 추가
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-University"] = "을지대학교"
        response.headers["X-Project"] = "을GPT"
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"을지대학교 을GPT 요청 오류 - "
            f"ID: {request_id} | "
            f"Error: {str(e)} | "
            f"Time: {process_time:.4f}s"
        )
        raise

# 2. 을지대학교 을GPT 보안 미들웨어
@app.middleware("http")
async def eulji_gpt_security_middleware(request: Request, call_next: Callable):
    """
    을지대학교 을GPT 보안 헤더 추가 미들웨어
    """
    response = await call_next(request)
    
    # 보안 헤더 추가
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response

# 3. 을지대학교 을GPT 접근 제한 미들웨어
@app.middleware("http")
async def eulji_gpt_access_control_middleware(request: Request, call_next: Callable):
    """
    을지대학교 을GPT 접근 제한 미들웨어
    특정 경로나 시간대에 대한 접근 제어
    """
    current_hour = datetime.now().hour
    
    # 의료 데이터 관련 API는 업무 시간 (9-18시)에만 접근 허용
    if "/medical" in str(request.url) and not (9 <= current_hour <= 18):
        logger.warning(f"업무 시간 외 의료 데이터 접근 시도: {request.client.host}")
        raise HTTPException(
            status_code=403,
            detail="의료 데이터는 업무 시간(09:00-18:00)에만 접근 가능합니다."
        )
    
    # 관리자 페이지는 을지대학교 IP 대역에서만 접근 허용 (예시)
    if "/admin" in str(request.url):
        client_ip = request.client.host if request.client else "unknown"
        allowed_ips = ["127.0.0.1", "::1"]  # 실제로는 을지대학교 IP 대역 설정
        
        if client_ip not in allowed_ips:
            logger.warning(f"허용되지 않은 IP에서 관리자 페이지 접근: {client_ip}")
            raise HTTPException(
                status_code=403,
                detail="관리자 페이지는 을지대학교 내부 네트워크에서만 접근 가능합니다."
            )
    
    return await call_next(request)

# 4. 을지대학교 을GPT 데이터베이스 로깅 미들웨어
@app.middleware("http")
async def eulji_gpt_db_logging_middleware(request: Request, call_next: Callable):
    """
    을지대학교 을GPT 데이터베이스 접근 로깅 미들웨어
    """
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # 데이터베이스에 접근 로그 저장 (비동기로 처리)
    try:
        # 실제 구현에서는 비동기 태스크로 처리하는 것이 좋습니다
        pass  # AccessLog 모델을 사용한 로깅 구현
    except Exception as e:
        logger.error(f"DB 로깅 실패: {str(e)}")
    
    return response

# 5. 을지대학교 을GPT 성능 모니터링 미들웨어
class PerformanceMonitoringMiddleware:
    """
    을지대학교 을GPT 성능 모니터링 미들웨어 클래스
    """
    def __init__(self, app: FastAPI):
        self.app = app
        self.request_counts = {}
        self.response_times = {}
    
    async def __call__(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        # 요청 카운트
        path = str(request.url.path)
        self.request_counts[path] = self.request_counts.get(path, 0) + 1
        
        response = await call_next(request)
        
        # 응답 시간 기록
        process_time = time.time() - start_time
        if path not in self.response_times:
            self.response_times[path] = []
        self.response_times[path].append(process_time)
        
        # 느린 요청 알림 (1초 초과)
        if process_time > 1.0:
            logger.warning(
                f"을지대학교 을GPT 느린 요청 감지 - "
                f"Path: {path} | Time: {process_time:.4f}s"
            )
        
        return response

# 미들웨어 등록
app.add_middleware(PerformanceMonitoringMiddleware)

# 내장 미들웨어 설정
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.eulji.ac.kr"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://eulji.ac.kr", "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time", "X-Request-ID", "X-University", "X-Project"]
)

# 테스트 엔드포인트들
@app.get("/")
def read_root():
    """을지대학교 을GPT 홈페이지"""
    return {
        "message": "을지대학교 을GPT 미들웨어 시스템에 오신 것을 환영합니다!",
        "university": "을지대학교",
        "project": "을GPT",
        "timestamp": datetime.now()
    }

@app.get("/students/", response_model=list[EuljiStudentInDB])
def get_students(db: Session = Depends(get_db)):
    """을지대학교 학생 목록 (미들웨어 테스트용)"""
    students = db.query(EuljiStudent).limit(10).all()
    return students

@app.get("/medical/patient-data")
def get_patient_data():
    """의료 데이터 API (시간 제한 테스트용)"""
    return {
        "message": "의료 데이터에 접근했습니다.",
        "warning": "이 API는 업무 시간(09:00-18:00)에만 접근 가능합니다.",
        "access_time": datetime.now()
    }

@app.get("/admin/dashboard")
def admin_dashboard():
    """관리자 대시보드 (IP 제한 테스트용)"""
    return {
        "message": "을지대학교 을GPT 관리자 대시보드",
        "warning": "이 페이지는 을지대학교 내부 네트워크에서만 접근 가능합니다.",
        "access_time": datetime.now()
    }

@app.get("/slow-endpoint")
async def slow_endpoint():
    """느린 엔드포인트 (성능 모니터링 테스트용)"""
    import asyncio
    await asyncio.sleep(1.5)  # 1.5초 지연
    return {
        "message": "이 엔드포인트는 의도적으로 느립니다.",
        "delay": "1.5초"
    }

@app.get("/stats/performance")
def get_performance_stats():
    """성능 통계 조회"""
    # 실제 구현에서는 PerformanceMonitoringMiddleware 인스턴스에서 데이터 가져오기
    return {
        "message": "을지대학교 을GPT 성능 통계",
        "note": "실제 통계는 미들웨어에서 수집됩니다.",
        "timestamp": datetime.now()
    }

@app.get("/test/headers")
def test_headers(request: Request):
    """헤더 테스트 엔드포인트"""
    return {
        "message": "요청 헤더 정보",
        "user_agent": request.headers.get("user-agent"),
        "x_request_id": request.headers.get("x-request-id"),
        "all_headers": dict(request.headers)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
