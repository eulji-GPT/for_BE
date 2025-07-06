"""
Step 03: 경로 매개변수
을지대학교 을GPT - 경로 매개변수를 사용한 동적 API 엔드포인트
"""

from fastapi import FastAPI, Path, HTTPException
from datetime import datetime
from typing import Optional

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="을지대학교 을GPT - Step 03",
    description="을지대학교 을GPT 프로젝트 - 경로 매개변수를 사용한 동적 API",
    version="1.0.0"
)

# 을지대학교 샘플 데이터
eulji_students = {
    1: {"id": 1, "name": "김을지", "major": "간호학과", "grade": 3, "city": "대전"},
    2: {"id": 2, "name": "을량이", "major": "방사선학과", "grade": 2, "city": "서울"},
    3: {"id": 3, "name": "안건", "major": "의료IT학과", "grade": 4, "city": "성남"}
}

eulji_projects = {
    1: {"id": 1, "name": "을GPT", "category": "AI프로젝트", "status": "진행중", "team": "을지대학교"},
    2: {"id": 2, "name": "스마트캠퍼스", "category": "웹개발", "status": "완료", "team": "을지대학교"},
    3: {"id": 3, "name": "모바일앱", "category": "앱개발", "status": "계획중", "team": "을지대학교"}
}

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    """
    을지대학교 을GPT - 기본 루트 경로
    """
    return {"message": "을지대학교 을GPT - FastAPI Step 03", "university": "을지대학교"}

# 단일 경로 매개변수 - 학생 정보 조회
@app.get("/students/{student_id}")
def get_student(student_id: int = Path(..., gt=0, description="학생 ID")):
    """
    을지대학교 학생 ID를 통해 특정 학생 정보를 조회하는 엔드포인트
    """
    if student_id not in eulji_students:
        raise HTTPException(status_code=404, detail="을지대학교에서 해당 학생을 찾을 수 없습니다")
    
    return {"student": eulji_students[student_id], "university": "을지대학교"}

# 단일 경로 매개변수 - 프로젝트 정보 조회
@app.get("/projects/{project_id}")
def get_project(project_id: int = Path(..., gt=0, le=1000, description="프로젝트 ID")):
    """
    을지대학교 프로젝트 ID를 통해 특정 프로젝트 정보를 조회하는 엔드포인트
    """
    if project_id not in eulji_projects:
        raise HTTPException(status_code=404, detail="을지대학교에서 해당 프로젝트를 찾을 수 없습니다")
    
    return {"project": eulji_projects[project_id], "university": "을지대학교"}

# 문자열 경로 매개변수 - 을지대학교 인사말
@app.get("/greet/{name}")
def greet_eulji_student(name: str = Path(..., min_length=1, max_length=50, description="학생 이름")):
    """
    을지대학교 학생 이름을 받아 인사말을 반환하는 엔드포인트
    """
    return {
        "message": f"안녕하세요, {name}님! 을지대학교 을GPT 프로젝트에 오신 것을 환영합니다!",
        "timestamp": datetime.now().isoformat(),
        "university": "을지대학교"
    }

# 여러 경로 매개변수 - 을GPT 계산기
@app.get("/calculate/{operation}/{num1}/{num2}")
def eulji_calculate(
    operation: str = Path(..., description="연산 종류 (add, subtract, multiply, divide)"),
    num1: float = Path(..., description="첫 번째 숫자"),
    num2: float = Path(..., description="두 번째 숫자")
):
    """
    을지대학교 을GPT - 두 숫자로 계산을 수행하는 엔드포인트
    """
    operations = {
        "add": num1 + num2,
        "subtract": num1 - num2,
        "multiply": num1 * num2,
        "divide": num1 / num2 if num2 != 0 else None
    }
    
    if operation not in operations:
        raise HTTPException(status_code=400, detail="을지대학교 을GPT - 지원하지 않는 연산입니다")
    
    if operation == "divide" and num2 == 0:
        raise HTTPException(status_code=400, detail="을지대학교 을GPT - 0으로 나눌 수 없습니다")
    
    return {
        "operation": operation,
        "operand1": num1,
        "operand2": num2,
        "result": operations[operation],
        "calculated_by": "을지대학교 을GPT 계산기"
    }

# 경로 매개변수와 쿼리 매개변수 조합 - 을지대학교 학생 프로필
@app.get("/students/{student_id}/profile")
def get_eulji_student_profile(
    student_id: int = Path(..., gt=0, description="을지대학교 학생 ID"),
    include_details: bool = False
):
    """
    을지대학교 학생의 프로필 정보를 조회하는 엔드포인트
    """
    if student_id not in eulji_students:
        raise HTTPException(status_code=404, detail="을지대학교에서 해당 학생을 찾을 수 없습니다")
    
    student = eulji_students[student_id].copy()
    
    if include_details:
        student["profile_created"] = datetime.now().isoformat()
        student["status"] = "을지대학교 재학생"
        student["university"] = "을지대학교"
    
    return {"profile": student, "university": "을지대학교"}

# 파일 경로 매개변수 예제 - 을지대학교
@app.get("/eulji-files/{file_path:path}")
def read_eulji_file(file_path: str):
    """
    을지대학교 을GPT - 파일 경로를 받아 처리하는 엔드포인트
    """
    return {
        "file_path": file_path,
        "message": f"을지대학교 을GPT - 파일 경로: {file_path}",
        "university": "을지대학교"
    }

# 카테고리별 프로젝트 조회 - 을지대학교
@app.get("/categories/{category}/projects")
def get_eulji_projects_by_category(category: str = Path(..., description="을지대학교 프로젝트 카테고리")):
    """
    을지대학교 카테고리별로 프로젝트를 조회하는 엔드포인트
    """
    category_projects = [
        project for project in eulji_projects.values()
        if project["category"].lower() == category.lower()
    ]
    
    return {
        "category": category,
        "projects": category_projects,
        "count": len(category_projects),
        "university": "을지대학교"
    }

# 학년별 학생 조회 - 을지대학교
@app.get("/students/grade/{min_grade}/{max_grade}")
def get_eulji_students_by_grade(
    min_grade: int = Path(..., ge=1, le=4, description="최소 학년"),
    max_grade: int = Path(..., ge=1, le=4, description="최대 학년")
):
    """
    을지대학교 학년 범위로 학생을 조회하는 엔드포인트
    """
    if min_grade > max_grade:
        raise HTTPException(status_code=400, detail="을지대학교 을GPT - 최소 학년이 최대 학년보다 클 수 없습니다")
    
    filtered_students = [
        student for student in eulji_students.values()
        if min_grade <= student["grade"] <= max_grade
    ]
    
    return {
        "grade_range": f"{min_grade}-{max_grade}학년",
        "students": filtered_students,
        "count": len(filtered_students),
        "university": "을지대학교"
    }

# 서버 실행 코드 (개발용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
