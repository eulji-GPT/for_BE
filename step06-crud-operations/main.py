"""
을지대학교 을GPT - Step 06: CRUD 작업
Create, Read, Update, Delete 작업을 체계적으로 구현
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import SessionLocal, engine
from models import EuljiStudent, EuljiProject
from schemas import (
    EuljiStudentCreate, EuljiStudentUpdate, EuljiStudentInDB,
    EuljiProjectCreate, EuljiProjectUpdate, EuljiProjectInDB,
    EuljiMajor, ProjectStatus
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="을지대학교 을GPT - CRUD API",
    description="을지대학교 을GPT 프로젝트의 CRUD 작업 실습",
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

# 을지대학교 학생 CRUD 엔드포인트
@app.post("/students/", response_model=EuljiStudentInDB, status_code=201)
def create_eulji_student(
    student: EuljiStudentCreate, 
    db: Session = Depends(get_db)
):
    """을지대학교 학생 데이터 생성"""
    try:
        # 학번 중복 체크
        existing_student = db.query(EuljiStudent).filter(
            EuljiStudent.student_number == student.student_number
        ).first()
        if existing_student:
            raise HTTPException(status_code=400, detail="이미 존재하는 학번입니다.")
        
        db_student = EuljiStudent(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        
        logger.info(f"을지대학교 학생 생성됨: {db_student.name} ({db_student.student_number})")
        return db_student
        
    except Exception as e:
        db.rollback()
        logger.error(f"학생 생성 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="학생 생성에 실패했습니다.")

@app.get("/students/", response_model=List[EuljiStudentInDB])
def get_eulji_students(
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 항목 수"),
    major: Optional[EuljiMajor] = Query(None, description="전공별 필터"),
    grade: Optional[int] = Query(None, ge=1, le=4, description="학년별 필터"),
    search: Optional[str] = Query(None, description="이름 검색"),
    db: Session = Depends(get_db)
):
    """을지대학교 학생 목록 조회 (필터링, 페이지네이션, 검색 포함)"""
    query = db.query(EuljiStudent)
    
    # 필터링
    if major:
        query = query.filter(EuljiStudent.major == major)
    if grade:
        query = query.filter(EuljiStudent.grade == grade)
    if search:
        query = query.filter(EuljiStudent.name.contains(search))
    
    # 페이지네이션
    students = query.offset(skip).limit(limit).all()
    
    logger.info(f"을지대학교 학생 목록 조회: {len(students)}명")
    return students

@app.get("/students/major/{major}", response_model=List[EuljiStudentInDB])
def get_students_by_major(
    major: EuljiMajor,
    db: Session = Depends(get_db)
):
    """전공별 을지대학교 학생 조회"""
    students = db.query(EuljiStudent).filter(EuljiStudent.major == major).all()
    logger.info(f"{major} 학과 학생 조회: {len(students)}명")
    return students

@app.get("/students/{student_id}", response_model=EuljiStudentInDB)
def get_eulji_student(student_id: int, db: Session = Depends(get_db)):
    """을지대학교 학생 개별 조회"""
    student = db.query(EuljiStudent).filter(EuljiStudent.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    
    logger.info(f"을지대학교 학생 조회: {student.name}")
    return student

@app.put("/students/{student_id}", response_model=EuljiStudentInDB)
def update_eulji_student(
    student_id: int,
    student_update: EuljiStudentUpdate,
    db: Session = Depends(get_db)
):
    """을지대학교 학생 정보 수정"""
    student = db.query(EuljiStudent).filter(EuljiStudent.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    
    # 업데이트할 필드만 수정
    update_data = student_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    try:
        db.commit()
        db.refresh(student)
        logger.info(f"을지대학교 학생 정보 수정: {student.name}")
        return student
    except Exception as e:
        db.rollback()
        logger.error(f"학생 정보 수정 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="학생 정보 수정에 실패했습니다.")

@app.delete("/students/{student_id}")
def delete_eulji_student(student_id: int, db: Session = Depends(get_db)):
    """을지대학교 학생 삭제"""
    student = db.query(EuljiStudent).filter(EuljiStudent.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다.")
    
    try:
        db.delete(student)
        db.commit()
        logger.info(f"을지대학교 학생 삭제: {student.name}")
        return {"message": "학생이 성공적으로 삭제되었습니다."}
    except Exception as e:
        db.rollback()
        logger.error(f"학생 삭제 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="학생 삭제에 실패했습니다.")

# 을지대학교 을GPT 프로젝트 CRUD 엔드포인트
@app.post("/projects/", response_model=EuljiProjectInDB, status_code=201)
def create_eulji_project(
    project: EuljiProjectCreate,
    db: Session = Depends(get_db)
):
    """을지대학교 을GPT 프로젝트 생성"""
    try:
        db_project = EuljiProject(**project.dict())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        logger.info(f"을지대학교 을GPT 프로젝트 생성: {db_project.title}")
        return db_project
        
    except Exception as e:
        db.rollback()
        logger.error(f"프로젝트 생성 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="프로젝트 생성에 실패했습니다.")

@app.get("/projects/", response_model=List[EuljiProjectInDB])
def get_eulji_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[ProjectStatus] = Query(None, description="프로젝트 상태 필터"),
    category: Optional[str] = Query(None, description="프로젝트 카테고리 필터"),
    db: Session = Depends(get_db)
):
    """을지대학교 을GPT 프로젝트 목록 조회"""
    query = db.query(EuljiProject)
    
    if status:
        query = query.filter(EuljiProject.status == status)
    if category:
        query = query.filter(EuljiProject.category == category)
    
    projects = query.offset(skip).limit(limit).all()
    
    logger.info(f"을지대학교 을GPT 프로젝트 목록 조회: {len(projects)}개")
    return projects

@app.get("/projects/status/{status}", response_model=List[EuljiProjectInDB])
def get_projects_by_status(
    status: ProjectStatus,
    db: Session = Depends(get_db)
):
    """프로젝트 상태별 조회"""
    projects = db.query(EuljiProject).filter(EuljiProject.status == status).all()
    logger.info(f"{status} 상태 프로젝트 조회: {len(projects)}개")
    return projects

@app.put("/projects/{project_id}", response_model=EuljiProjectInDB)
def update_eulji_project(
    project_id: int,
    project_update: EuljiProjectUpdate,
    db: Session = Depends(get_db)
):
    """을지대학교 을GPT 프로젝트 수정"""
    project = db.query(EuljiProject).filter(EuljiProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다.")
    
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    try:
        db.commit()
        db.refresh(project)
        logger.info(f"을지대학교 을GPT 프로젝트 수정: {project.title}")
        return project
    except Exception as e:
        db.rollback()
        logger.error(f"프로젝트 수정 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="프로젝트 수정에 실패했습니다.")

# 통계 및 집계 엔드포인트
@app.get("/stats/students-by-major")
def get_students_stats_by_major(db: Session = Depends(get_db)):
    """전공별 학생 수 통계"""
    from sqlalchemy import func
    
    stats = db.query(
        EuljiStudent.major,
        func.count(EuljiStudent.id).label('student_count')
    ).group_by(EuljiStudent.major).all()
    
    result = {major: count for major, count in stats}
    logger.info(f"전공별 학생 통계 조회: {result}")
    return result

@app.get("/stats/projects-by-status")
def get_projects_stats_by_status(db: Session = Depends(get_db)):
    """상태별 프로젝트 수 통계"""
    from sqlalchemy import func
    
    stats = db.query(
        EuljiProject.status,
        func.count(EuljiProject.id).label('project_count')
    ).group_by(EuljiProject.status).all()
    
    result = {status: count for status, count in stats}
    logger.info(f"상태별 프로젝트 통계 조회: {result}")
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
