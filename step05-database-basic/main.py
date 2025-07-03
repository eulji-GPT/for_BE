"""
Step 05: 데이터베이스 기초
SQLAlchemy를 사용한 데이터베이스 연결 및 기본 작업 예제입니다.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# 로컬 모듈 import
from database import get_db, create_database
from models import User, Product
from schemas import UserCreate, UserInDB, UserUpdate, ProductCreate, ProductInDB, ProductUpdate

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="FastAPI 튜토리얼 - Step 05",
    description="SQLAlchemy를 사용한 데이터베이스 기초",
    version="1.0.0"
)

# 애플리케이션 시작 시 데이터베이스 테이블 생성
@app.on_event("startup")
def startup_event():
    create_database()

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    """
    기본 루트 경로
    """
    return {"message": "FastAPI Step 05 - 데이터베이스 기초 예제"}

# 데이터베이스 연결 테스트
@app.get("/db-test")
def test_database_connection(db: Session = Depends(get_db)):
    """
    데이터베이스 연결을 테스트하는 엔드포인트
    """
    try:
        # 간단한 쿼리 실행으로 연결 확인
        result = db.execute("SELECT 1").fetchone()
        return {
            "status": "success",
            "message": "데이터베이스 연결이 성공했습니다",
            "result": result[0] if result else None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터베이스 연결 실패: {str(e)}"
        )

# 사용자 관련 엔드포인트
@app.post("/users/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    새로운 사용자를 생성하는 엔드포인트
    """
    # 이메일 중복 확인
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )
    
    # 새 사용자 생성
    db_user = User(
        name=user.name,
        email=user.email,
        age=user.age
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.get("/users/", response_model=List[UserInDB])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    사용자 목록을 조회하는 엔드포인트
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserInDB)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    특정 사용자를 조회하는 엔드포인트
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    return user

@app.put("/users/{user_id}", response_model=UserInDB)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    사용자 정보를 업데이트하는 엔드포인트
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    # 업데이트할 필드만 적용
    update_data = user_update.dict(exclude_unset=True)
    
    # 이메일 중복 확인 (변경하려는 경우)
    if "email" in update_data:
        existing_user = db.query(User).filter(
            User.email == update_data["email"],
            User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 등록된 이메일입니다"
            )
    
    # 필드 업데이트
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    사용자를 삭제하는 엔드포인트
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    db.delete(db_user)
    db.commit()
    
    return {"message": "사용자가 성공적으로 삭제되었습니다"}

# 제품 관련 엔드포인트
@app.post("/products/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    새로운 제품을 생성하는 엔드포인트
    """
    db_product = Product(
        name=product.name,
        description=product.description,
        price=int(product.price * 100),  # 센트 단위로 저장
        category=product.category
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product

@app.get("/products/", response_model=List[ProductInDB])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    제품 목록을 조회하는 엔드포인트
    """
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=ProductInDB)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    특정 제품을 조회하는 엔드포인트
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="제품을 찾을 수 없습니다"
        )
    return product

# 통계 엔드포인트
@app.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    """
    데이터베이스 통계를 조회하는 엔드포인트
    """
    user_count = db.query(User).count()
    active_user_count = db.query(User).filter(User.is_active == True).count()
    product_count = db.query(Product).count()
    available_product_count = db.query(Product).filter(Product.is_available == True).count()
    
    return {
        "users": {
            "total": user_count,
            "active": active_user_count
        },
        "products": {
            "total": product_count,
            "available": available_product_count
        }
    }

# 서버 실행 코드 (개발용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
