"""
Step 04: 요청 본문
을지대학교 을GPT - Pydantic 모델을 사용한 요청 본문 처리
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="을지대학교 을GPT - Step 04",
    description="을지대학교 을GPT 프로젝트 - 요청 본문과 Pydantic 모델을 사용한 API",
    version="1.0.0"
)

# 을지대학교 전공 및 역할 열거형 정의
class EuljiMajor(str, Enum):
    nursing = "간호학과"
    radiology = "방사선학과"
    medical_it = "의료IT학과"
    physical_therapy = "물리치료학과"

class StudentRole(str, Enum):
    student = "학생"
    admin = "관리자"
    professor = "교수"
    assistant = "조교"

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
    user_id: int
    items: List[OrderItem]
    total_amount: float
    notes: Optional[str]
    created_at: datetime
    status: str = "pending"

# 메모리 저장소 (실제 개발에서는 데이터베이스 사용)
users_db = {}
products_db = {}
orders_db = {}
next_user_id = 1
next_product_id = 1
next_order_id = 1

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    """
    기본 루트 경로
    """
    return {"message": "FastAPI Step 04 - 요청 본문 처리 예제"}

# 사용자 관련 엔드포인트
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """
    새로운 사용자를 생성하는 엔드포인트
    """
    global next_user_id
    
    # 이메일 중복 확인
    for existing_user in users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 이메일입니다"
            )
    
    # 사용자 생성
    user_data = user.dict(exclude={"password", "confirm_password"})
    user_data.update({
        "id": next_user_id,
        "created_at": datetime.now(),
        "is_active": True
    })
    
    users_db[next_user_id] = user_data
    next_user_id += 1
    
    return user_data

@app.get("/users/", response_model=List[UserResponse])
def get_users():
    """
    모든 사용자 목록을 조회하는 엔드포인트
    """
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    특정 사용자를 조회하는 엔드포인트
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    return users_db[user_id]

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    """
    사용자 정보를 업데이트하는 엔드포인트
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    # 업데이트할 데이터만 가져오기
    update_data = user_update.dict(exclude_unset=True)
    
    # 이메일 중복 확인
    if "email" in update_data:
        for uid, existing_user in users_db.items():
            if uid != user_id and existing_user["email"] == update_data["email"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="이미 존재하는 이메일입니다"
                )
    
    # 사용자 정보 업데이트
    users_db[user_id].update(update_data)
    return users_db[user_id]

# 제품 관련 엔드포인트
@app.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    """
    새로운 제품을 생성하는 엔드포인트
    """
    global next_product_id
    
    product_data = product.dict()
    product_data.update({
        "id": next_product_id,
        "created_at": datetime.now()
    })
    
    products_db[next_product_id] = product_data
    next_product_id += 1
    
    return product_data

@app.get("/products/", response_model=List[ProductResponse])
def get_products():
    """
    모든 제품 목록을 조회하는 엔드포인트
    """
    return list(products_db.values())

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """
    특정 제품을 조회하는 엔드포인트
    """
    if product_id not in products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="제품을 찾을 수 없습니다"
        )
    return products_db[product_id]

# 주문 관련 엔드포인트
@app.post("/orders/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    """
    새로운 주문을 생성하는 엔드포인트
    """
    global next_order_id
    
    # 사용자 존재 확인
    if order.user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    # 제품 존재 확인 및 총액 계산
    total_amount = 0
    for item in order.items:
        if item.product_id not in products_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"제품 ID {item.product_id}를 찾을 수 없습니다"
            )
        
        product = products_db[item.product_id]
        if not product["is_available"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"제품 '{product['name']}'은 현재 판매중이지 않습니다"
            )
        
        total_amount += product["price"] * item.quantity
    
    # 주문 생성
    order_data = order.dict()
    order_data.update({
        "id": next_order_id,
        "total_amount": total_amount,
        "created_at": datetime.now(),
        "status": "pending"
    })
    
    orders_db[next_order_id] = order_data
    next_order_id += 1
    
    return order_data

@app.get("/orders/", response_model=List[OrderResponse])
def get_orders():
    """
    모든 주문 목록을 조회하는 엔드포인트
    """
    return list(orders_db.values())

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    """
    특정 주문을 조회하는 엔드포인트
    """
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="주문을 찾을 수 없습니다"
        )
    return orders_db[order_id]

# 복잡한 요청 본문 예제
class ComplexData(BaseModel):
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    is_published: bool = False
    
@app.post("/complex-data/")
def process_complex_data(data: ComplexData):
    """
    복잡한 데이터 구조를 처리하는 엔드포인트
    """
    return {
        "message": "복잡한 데이터가 성공적으로 처리되었습니다",
        "processed_data": data.dict(),
        "timestamp": datetime.now().isoformat()
    }

# 서버 실행 코드 (개발용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
