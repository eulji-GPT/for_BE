"""
Step 04: 요청 본문
을지대학교 을GPT - Pydantic 모델을 사용한 요청 본문 처리
"""

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="을지대학교 을GPT - Step 04",
    description="을지대학교 을GPT 프로젝트 - 요청 본문과 Pydantic 모델을 사용한 API",
    version="1.0.0"
)

# 422 오류에 대한 커스텀 핸들러 추가
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "유효성 검사 실패",
            "errors": exc.errors(),
            "message": "입력 데이터를 확인해주세요"
        }
    )

# 을지대학교 전공 및 역할 열거형 정의
class EuljiMajor(str, Enum):
    nursing = "nursing"
    radiology = "radiology"
    medical_it = "medical_it"
    physical_therapy = "physical_therapy"

class StudentRole(str, Enum):
    student = "student"
    admin = "admin"
    professor = "professor"
    assistant = "assistant"

class ProjectCategory(str, Enum):
    ai = "AI프로젝트"
    web = "웹개발"
    mobile = "모바일앱"
    healthcare = "의료시스템"

# 을지대학교 학생 모델 정의
class EuljiStudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="학생 이름")
    email: EmailStr = Field(..., description="이메일 주소")
    student_id: str = Field(..., min_length=8, max_length=12, description="학번")
    major: EuljiMajor = Field(..., description="전공")
    grade: int = Field(..., ge=1, le=4, description="학년")
    role: StudentRole = Field(default=StudentRole.student, description="역할")
    
    @validator('student_id')
    def validate_student_id(cls, v):
        if not v.isdigit():
            raise ValueError('학번은 숫자만 포함해야 합니다')
        return v

class EuljiStudentCreate(EuljiStudentBase):
    password: str = Field(..., min_length=8, description="비밀번호 (8자 이상)")
    confirm_password: str = Field(..., description="비밀번호 확인")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v

class EuljiStudentResponse(EuljiStudentBase):
    id: int
    created_at: datetime
    is_active: bool = True

class EuljiStudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    major: Optional[EuljiMajor] = None
    grade: Optional[int] = Field(None, ge=1, le=4)
    role: Optional[StudentRole] = None

class EuljiProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="프로젝트명")
    description: Optional[str] = Field(None, max_length=1000, description="프로젝트 설명")
    category: ProjectCategory = Field(..., description="카테고리")
    team_size: int = Field(..., gt=0, le=10, description="팀 크기")
    is_active: bool = Field(default=True, description="활성 상태")

class EuljiProjectCreate(EuljiProjectBase):
    pass

class EuljiProjectResponse(EuljiProjectBase):
    id: int
    created_at: datetime

class ProjectMember(BaseModel):
    student_id: int = Field(..., gt=0, description="학생 ID")
    role: str = Field(..., description="역할")
    
class ProjectTeamCreate(BaseModel):
    project_id: int = Field(..., gt=0, description="프로젝트 ID")
    members: List[ProjectMember] = Field(..., min_items=1, description="팀 멤버")
    notes: Optional[str] = Field(None, max_length=500, description="비고")

class ProjectTeamResponse(BaseModel):
    id: int
    project_id: int
    members: List[ProjectMember]
    notes: Optional[str]
    created_at: datetime
    status: str = "active"

# 복잡한 요청 본문 예제
class EuljiComplexData(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="제목")
    content: str = Field(..., min_length=1, description="내용")
    tags: List[str] = Field(default_factory=list, description="태그")
    metadata: dict = Field(default_factory=dict, description="메타데이터")
    is_published: bool = Field(default=False, description="게시 여부")

# 메모리 저장소 (실제 개발에서는 데이터베이스 사용)
students_db = {}
projects_db = {}
teams_db = {}
next_student_id = 1
next_project_id = 1
next_team_id = 1

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    """
    을지대학교 을GPT - 기본 루트 경로
    """
    return {
        "message": "을지대학교 을GPT - Step 04 요청 본문 처리", 
        "university": "을지대학교",
        "project": "을GPT"
    }

# 을지대학교 학생 관련 엔드포인트
@app.post("/students/", response_model=EuljiStudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: EuljiStudentCreate):
    """
    새로운 을지대학교 학생을 등록하는 엔드포인트
    """
    global next_student_id
    
    # 이메일 및 학번 중복 확인
    for existing_student in students_db.values():
        if existing_student["email"] == student.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 등록된 이메일입니다"
            )
        if existing_student["student_id"] == student.student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 등록된 학번입니다"
            )
    
    # 학생 정보 생성
    student_data = student.dict(exclude={"password", "confirm_password"})
    student_data.update({
        "id": next_student_id,
        "created_at": datetime.now(),
        "is_active": True
    })
    
    students_db[next_student_id] = student_data
    next_student_id += 1
    
    return student_data

@app.get("/students/", response_model=List[EuljiStudentResponse])
def get_students():
    """
    모든 을지대학교 학생 목록을 조회하는 엔드포인트
    """
    return list(students_db.values())

@app.get("/students/{student_id}", response_model=EuljiStudentResponse)
def get_student(student_id: int):
    """
    특정 을지대학교 학생을 조회하는 엔드포인트
    """
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="학생을 찾을 수 없습니다"
        )
    return students_db[student_id]

@app.put("/students/{student_id}", response_model=EuljiStudentResponse)
def update_student(student_id: int, student_update: EuljiStudentUpdate):
    """
    을지대학교 학생 정보를 업데이트하는 엔드포인트
    """
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="학생을 찾을 수 없습니다"
        )
    
    # 업데이트할 데이터만 가져오기
    update_data = student_update.dict(exclude_unset=True)
    
    # 이메일 중복 확인 (변경하려는 경우)
    if "email" in update_data:
        for sid, existing_student in students_db.items():
            if sid != student_id and existing_student["email"] == update_data["email"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="이미 등록된 이메일입니다"
                )
    
    # 학생 정보 업데이트
    students_db[student_id].update(update_data)
    return students_db[student_id]

# 을지대학교 프로젝트 관련 엔드포인트
@app.post("/projects/", response_model=EuljiProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: EuljiProjectCreate):
    """
    새로운 을지대학교 을GPT 프로젝트를 생성하는 엔드포인트
    """
    global next_project_id
    
    project_data = project.dict()
    project_data.update({
        "id": next_project_id,
        "created_at": datetime.now()
    })
    
    projects_db[next_project_id] = project_data
    next_project_id += 1
    
    return project_data

@app.get("/projects/", response_model=List[EuljiProjectResponse])
def get_projects():
    """
    모든 을지대학교 을GPT 프로젝트 목록을 조회하는 엔드포인트
    """
    return list(projects_db.values())

@app.get("/projects/{project_id}", response_model=EuljiProjectResponse)
def get_project(project_id: int):
    """
    특정 을지대학교 을GPT 프로젝트를 조회하는 엔드포인트
    """
    if project_id not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="프로젝트를 찾을 수 없습니다"
        )
    return projects_db[project_id]

# 프로젝트 팀 관련 엔드포인트
@app.post("/teams/", response_model=ProjectTeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(team: ProjectTeamCreate):
    """
    새로운 프로젝트 팀을 생성하는 엔드포인트
    """
    global next_team_id
    
    # 프로젝트 존재 확인
    if team.project_id not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="프로젝트를 찾을 수 없습니다"
        )
    
    # 팀 멤버 존재 확인
    for member in team.members:
        if member.student_id not in students_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"학생 ID {member.student_id}를 찾을 수 없습니다"
            )
    
    # 팀 생성
    team_data = team.dict()
    team_data.update({
        "id": next_team_id,
        "created_at": datetime.now(),
        "status": "active"
    })
    
    teams_db[next_team_id] = team_data
    next_team_id += 1
    
    return team_data

@app.get("/teams/", response_model=List[ProjectTeamResponse])
def get_teams():
    """
    모든 프로젝트 팀 목록을 조회하는 엔드포인트
    """
    return list(teams_db.values())

@app.get("/teams/{team_id}", response_model=ProjectTeamResponse)
def get_team(team_id: int):
    """
    특정 프로젝트 팀을 조회하는 엔드포인트
    """
    if team_id not in teams_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="팀을 찾을 수 없습니다"
        )
    return teams_db[team_id]

# 복잡한 요청 본문 예제
@app.post("/complex-data/")
def process_complex_data(data: EuljiComplexData):
    """
    을지대학교 을GPT - 복잡한 데이터 구조를 처리하는 엔드포인트
    """
    return {
        "message": "을지대학교 을GPT - 복잡한 데이터가 성공적으로 처리되었습니다",
        "university": "을지대학교",
        "project": "을GPT",
        "processed_data": data.dict(),
        "timestamp": datetime.now().isoformat()
    }

# 을지대학교 통계 엔드포인트
@app.get("/statistics")
def get_eulji_statistics():
    """
    을지대학교 을GPT 프로젝트 통계를 조회하는 엔드포인트
    """
    return {
        "university": "을지대학교",
        "project": "을GPT",
        "statistics": {
            "students": {
                "total": len(students_db),
                "active": sum(1 for s in students_db.values() if s.get("is_active", True))
            },
            "projects": {
                "total": len(projects_db),
                "active": sum(1 for p in projects_db.values() if p.get("is_active", True))
            },
            "teams": {
                "total": len(teams_db),
                "active": sum(1 for t in teams_db.values() if t.get("status") == "active")
            }
        }
    }

# 서버 실행 코드 (개발용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
