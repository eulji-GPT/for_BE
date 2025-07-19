"""
을지대학교 을GPT - Step 07: JWT 토큰 기반 인증 시스템
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import logging

from jose import JWTError, jwt
from passlib.context import CryptContext

from database import SessionLocal, engine
from models import EuljiStudent, EuljiProject
from schemas import (
    EuljiStudentCreate, EuljiStudentLogin, EuljiStudentInDB,
    Token, TokenData, EuljiMajor
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT 설정
SECRET_KEY = "eulji-gpt-secret-key-for-authentication-system-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer 토큰
security = HTTPBearer()

app = FastAPI(
    title="을지대학교 을GPT - 인증 API",
    description="을지대학교 을GPT 프로젝트의 JWT 토큰 기반 인증 시스템",
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

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 비밀번호 해싱 함수들
def verify_password(plain_password, hashed_password):
    """비밀번호 검증"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """비밀번호 해싱"""
    return pwd_context.hash(password)

def authenticate_eulji_student(db: Session, student_number: str, password: str):
    """을지대학교 학생 인증"""
    student = db.query(EuljiStudent).filter(
        EuljiStudent.student_number == student_number
    ).first()
    
    if not student:
        return False
    if not verify_password(password, student.password_hash):
        return False
    return student

def create_eulji_access_token(student_data: dict, expires_delta: Optional[timedelta] = None):
    """을지대학교 을GPT JWT 토큰 생성"""
    to_encode = student_data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "university": "을지대학교",
        "project": "을GPT"
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_eulji_student(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """현재 인증된 을지대학교 학생 가져오기"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보를 확인할 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        student_number: str = payload.get("sub")
        if student_number is None:
            raise credentials_exception
        token_data = TokenData(student_number=student_number)
    except JWTError:
        raise credentials_exception
    
    student = db.query(EuljiStudent).filter(
        EuljiStudent.student_number == token_data.student_number
    ).first()
    if student is None:
        raise credentials_exception
    return student

async def get_current_active_eulji_student(
    current_student: EuljiStudent = Depends(get_current_eulji_student)
):
    """현재 활성화된 을지대학교 학생"""
    if not current_student.is_active:
        raise HTTPException(status_code=400, detail="비활성화된 계정입니다.")
    return current_student

# 권한 확인 함수들
def check_major_permission(required_major: EuljiMajor):
    """전공별 권한 확인"""
    def permission_checker(
        current_student: EuljiStudent = Depends(get_current_active_eulji_student)
    ):
        if current_student.major != required_major:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_major} 전공 학생만 접근 가능합니다."
            )
        return current_student
    return permission_checker

def check_grade_permission(minimum_grade: int):
    """학년별 권한 확인"""
    def permission_checker(
        current_student: EuljiStudent = Depends(get_current_active_eulji_student)
    ):
        if current_student.grade < minimum_grade:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{minimum_grade}학년 이상만 접근 가능합니다."
            )
        return current_student
    return permission_checker

# 인증 관련 엔드포인트
@app.post("/auth/register", response_model=EuljiStudentInDB, status_code=201)
def register_eulji_student(
    student: EuljiStudentCreate,
    db: Session = Depends(get_db)
):
    """을지대학교 학생 회원가입"""
    # 학번 중복 체크
    existing_student = db.query(EuljiStudent).filter(
        EuljiStudent.student_number == student.student_number
    ).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="이미 존재하는 학번입니다.")
    
    # 이메일 중복 체크
    existing_email = db.query(EuljiStudent).filter(
        EuljiStudent.email == student.email
    ).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="이미 사용중인 이메일입니다.")
    
    try:
        # 비밀번호 해싱
        student_data = student.dict()
        hashed_password = get_password_hash(student_data.pop("password"))
        
        db_student = EuljiStudent(
            **student_data,
            password_hash=hashed_password
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        
        logger.info(f"을지대학교 학생 회원가입: {db_student.name} ({db_student.student_number})")
        return db_student
        
    except Exception as e:
        db.rollback()
        logger.error(f"회원가입 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="회원가입에 실패했습니다.")

@app.post("/auth/student-login", response_model=Token)
def eulji_student_login(
    student_credentials: EuljiStudentLogin,
    db: Session = Depends(get_db)
):
    """을지대학교 학생 로그인"""
    student = authenticate_eulji_student(
        db, 
        student_credentials.student_number, 
        student_credentials.password
    )
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="학번 또는 비밀번호가 잘못되었습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not student.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 계정입니다."
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_eulji_access_token(
        student_data={
            "sub": student.student_number,
            "name": student.name,
            "major": student.major,
            "grade": student.grade
        },
        expires_delta=access_token_expires
    )
    
    logger.info(f"을지대학교 학생 로그인: {student.name} ({student.student_number})")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "student_info": {
            "name": student.name,
            "student_number": student.student_number,
            "major": student.major,
            "grade": student.grade
        }
    }

# 보호된 엔드포인트들
@app.get("/auth/me", response_model=EuljiStudentInDB)
def read_eulji_student_me(
    current_student: EuljiStudent = Depends(get_current_active_eulji_student)
):
    """현재 로그인된 을지대학교 학생 정보"""
    logger.info(f"을지대학교 학생 정보 조회: {current_student.name}")
    return current_student

@app.get("/protected/nursing-only")
def nursing_only_endpoint(
    current_student: EuljiStudent = Depends(check_major_permission(EuljiMajor.NURSING))
):
    """간호학과 전용 엔드포인트"""
    return {
        "message": f"안녕하세요, {current_student.name}님! 간호학과 전용 페이지입니다.",
        "major": current_student.major,
        "access_time": datetime.now()
    }

@app.get("/protected/senior-only")
def senior_only_endpoint(
    current_student: EuljiStudent = Depends(check_grade_permission(3))
):
    """3학년 이상 전용 엔드포인트"""
    return {
        "message": f"안녕하세요, {current_student.name}님! 3학년 이상 전용 페이지입니다.",
        "grade": current_student.grade,
        "access_time": datetime.now()
    }

@app.get("/protected/project-management")
def project_management_endpoint(
    current_student: EuljiStudent = Depends(get_current_active_eulji_student)
):
    """을지대학교 을GPT 프로젝트 관리 (로그인 필요)"""
    return {
        "message": f"안녕하세요, {current_student.name}님! 을지대학교 을GPT 프로젝트 관리 페이지입니다.",
        "student_info": {
            "name": current_student.name,
            "major": current_student.major,
            "grade": current_student.grade
        },
        "permissions": {
            "can_create_project": current_student.grade >= 2,
            "can_be_team_leader": current_student.grade >= 3,
            "can_mentor": current_student.grade == 4
        }
    }

@app.post("/auth/change-password")
def change_password(
    old_password: str,
    new_password: str,
    current_student: EuljiStudent = Depends(get_current_active_eulji_student),
    db: Session = Depends(get_db)
):
    """비밀번호 변경"""
    if not verify_password(old_password, current_student.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="현재 비밀번호가 일치하지 않습니다."
        )
    
    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="새 비밀번호는 8자 이상이어야 합니다."
        )
    
    try:
        current_student.password_hash = get_password_hash(new_password)
        db.commit()
        
        logger.info(f"비밀번호 변경: {current_student.name} ({current_student.student_number})")
        return {"message": "비밀번호가 성공적으로 변경되었습니다."}
        
    except Exception as e:
        db.rollback()
        logger.error(f"비밀번호 변경 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="비밀번호 변경에 실패했습니다.")

@app.post("/auth/logout")
def logout(
    current_student: EuljiStudent = Depends(get_current_active_eulji_student)
):
    """로그아웃 (클라이언트에서 토큰 삭제)"""
    logger.info(f"을지대학교 학생 로그아웃: {current_student.name}")
    return {"message": "성공적으로 로그아웃되었습니다."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
