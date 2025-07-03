"""
Step 03: 경로 매개변수
경로 매개변수를 사용한 동적 API 엔드포인트 예제입니다.
"""

from fastapi import FastAPI, Path, HTTPException
from datetime import datetime
from typing import Optional

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="FastAPI 튜토리얼 - Step 03",
    description="경로 매개변수를 사용한 동적 API 엔드포인트",
    version="1.0.0"
)

# 샘플 데이터
users = {
    1: {"id": 1, "name": "홍길동", "age": 30, "city": "서울"},
    2: {"id": 2, "name": "김철수", "age": 25, "city": "부산"},
    3: {"id": 3, "name": "이영희", "age": 28, "city": "대구"}
}

products = {
    1: {"id": 1, "name": "노트북", "price": 1200000, "category": "전자제품"},
    2: {"id": 2, "name": "마우스", "price": 25000, "category": "컴퓨터"},
    3: {"id": 3, "name": "키보드", "price": 80000, "category": "컴퓨터"}
}

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    """
    기본 루트 경로
    """
    return {"message": "FastAPI Step 03 - 경로 매개변수 예제"}

# 단일 경로 매개변수 - 사용자 정보 조회
@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., gt=0, description="사용자 ID")):
    """
    사용자 ID를 통해 특정 사용자 정보를 조회하는 엔드포인트
    """
    if user_id not in users:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    return {"user": users[user_id]}

# 단일 경로 매개변수 - 제품 정보 조회
@app.get("/products/{product_id}")
def get_product(product_id: int = Path(..., gt=0, le=1000, description="제품 ID")):
    """
    제품 ID를 통해 특정 제품 정보를 조회하는 엔드포인트
    """
    if product_id not in products:
        raise HTTPException(status_code=404, detail="제품을 찾을 수 없습니다")
    
    return {"product": products[product_id]}

# 문자열 경로 매개변수 - 인사말
@app.get("/greet/{name}")
def greet_user(name: str = Path(..., min_length=1, max_length=50, description="사용자 이름")):
    """
    이름을 받아 인사말을 반환하는 엔드포인트
    """
    return {
        "message": f"안녕하세요, {name}님!",
        "timestamp": datetime.now().isoformat()
    }

# 여러 경로 매개변수 - 계산기
@app.get("/calculate/{operation}/{num1}/{num2}")
def calculate(
    operation: str = Path(..., description="연산 종류 (add, subtract, multiply, divide)"),
    num1: float = Path(..., description="첫 번째 숫자"),
    num2: float = Path(..., description="두 번째 숫자")
):
    """
    두 숫자로 계산을 수행하는 엔드포인트
    """
    operations = {
        "add": num1 + num2,
        "subtract": num1 - num2,
        "multiply": num1 * num2,
        "divide": num1 / num2 if num2 != 0 else None
    }
    
    if operation not in operations:
        raise HTTPException(status_code=400, detail="지원하지 않는 연산입니다")
    
    if operation == "divide" and num2 == 0:
        raise HTTPException(status_code=400, detail="0으로 나눌 수 없습니다")
    
    return {
        "operation": operation,
        "operand1": num1,
        "operand2": num2,
        "result": operations[operation]
    }

# 경로 매개변수와 쿼리 매개변수 조합
@app.get("/users/{user_id}/profile")
def get_user_profile(
    user_id: int = Path(..., gt=0, description="사용자 ID"),
    include_details: bool = False
):
    """
    사용자의 프로필 정보를 조회하는 엔드포인트
    """
    if user_id not in users:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    user = users[user_id].copy()
    
    if include_details:
        user["profile_created"] = datetime.now().isoformat()
        user["status"] = "active"
    
    return {"profile": user}

# 파일 경로 매개변수 예제
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    """
    파일 경로를 받아 처리하는 엔드포인트
    """
    return {
        "file_path": file_path,
        "message": f"파일 경로: {file_path}"
    }

# 카테고리별 제품 조회
@app.get("/categories/{category}/products")
def get_products_by_category(category: str = Path(..., description="제품 카테고리")):
    """
    카테고리별로 제품을 조회하는 엔드포인트
    """
    category_products = [
        product for product in products.values()
        if product["category"].lower() == category.lower()
    ]
    
    return {
        "category": category,
        "products": category_products,
        "count": len(category_products)
    }

# 사용자 나이 그룹별 조회
@app.get("/users/age-group/{min_age}/{max_age}")
def get_users_by_age_group(
    min_age: int = Path(..., ge=0, le=120, description="최소 나이"),
    max_age: int = Path(..., ge=0, le=120, description="최대 나이")
):
    """
    나이 범위로 사용자를 조회하는 엔드포인트
    """
    if min_age > max_age:
        raise HTTPException(status_code=400, detail="최소 나이가 최대 나이보다 클 수 없습니다")
    
    filtered_users = [
        user for user in users.values()
        if min_age <= user["age"] <= max_age
    ]
    
    return {
        "age_range": f"{min_age}-{max_age}",
        "users": filtered_users,
        "count": len(filtered_users)
    }

# 서버 실행 코드 (개발용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
