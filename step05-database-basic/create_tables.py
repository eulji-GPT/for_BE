"""
SQLAlchemy를 사용한 테이블 생성 스크립트
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from database import Base, engine
import datetime

# 사용자 테이블 모델
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# 게시글 테이블 모델
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    author_id = Column(Integer, nullable=False)  # 실제로는 ForeignKey 사용 권장
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

def create_tables():
    """모든 테이블을 생성하는 함수"""
    print("🔧 데이터베이스 테이블 생성을 시작합니다...")
    
    try:
        # 테이블 생성
        Base.metadata.create_all(bind=engine)
        print("✅ 테이블 생성 성공!")
        
        # 생성된 테이블 확인
        print("\n📋 생성된 테이블:")
        print("✅ users - 사용자 정보 테이블")
        print("   - id (Primary Key)")
        print("   - username (고유)")
        print("   - email (고유)")
        print("   - full_name")
        print("   - is_active")
        print("   - created_at, updated_at")
        
        print("✅ posts - 게시글 테이블")
        print("   - id (Primary Key)")
        print("   - title")
        print("   - content")
        print("   - author_id")
        print("   - is_published")
        print("   - created_at, updated_at")
        
        return True
        
    except Exception as e:
        print(f"❌ 테이블 생성 실패: {e}")
        return False

def check_tables():
    """생성된 테이블을 확인하는 함수"""
    print("\n🔍 데이터베이스 테이블 확인 중...")
    
    try:
        from sqlalchemy import text
        
        with engine.connect() as connection:
            # 테이블 목록 조회
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print("📋 현재 데이터베이스의 테이블:")
                for table in tables:
                    print(f"   ✅ {table}")
                
                # 각 테이블의 구조 확인
                for table in tables:
                    print(f"\n🏗️  '{table}' 테이블 구조:")
                    result = connection.execute(text(f"DESCRIBE {table}"))
                    columns = result.fetchall()
                    for col in columns:
                        field_name = col[0]
                        field_type = col[1]
                        is_null = "NULL" if col[2] == "YES" else "NOT NULL"
                        key_info = f" ({col[3]})" if col[3] else ""
                        print(f"     - {field_name}: {field_type} {is_null}{key_info}")
                        
            else:
                print("❌ 테이블이 없습니다.")
                
    except Exception as e:
        print(f"❌ 테이블 확인 실패: {e}")

def insert_sample_data():
    """샘플 데이터를 삽입하는 함수"""
    print("\n📝 샘플 데이터 삽입 중...")
    
    try:
        from sqlalchemy.orm import sessionmaker
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 샘플 사용자 데이터
        sample_users = [
            User(
                username="admin",
                email="admin@example.com",
                full_name="관리자",
                is_active=True
            ),
            User(
                username="user1",
                email="user1@example.com",
                full_name="사용자 1",
                is_active=True
            ),
            User(
                username="user2",
                email="user2@example.com",
                full_name="사용자 2",
                is_active=False
            )
        ]
        
        # 사용자 데이터 추가
        for user in sample_users:
            db.add(user)
        
        db.commit()
        
        # 추가된 사용자 ID 가져오기
        users = db.query(User).all()
        
        # 샘플 게시글 데이터
        sample_posts = [
            Post(
                title="첫 번째 게시글",
                content="이것은 첫 번째 게시글의 내용입니다.",
                author_id=users[0].id,
                is_published=True
            ),
            Post(
                title="두 번째 게시글",
                content="이것은 두 번째 게시글의 내용입니다.",
                author_id=users[1].id,
                is_published=True
            ),
            Post(
                title="임시 저장된 게시글",
                content="아직 발행되지 않은 게시글입니다.",
                author_id=users[0].id,
                is_published=False
            )
        ]
        
        # 게시글 데이터 추가
        for post in sample_posts:
            db.add(post)
        
        db.commit()
        db.close()
        
        print("✅ 샘플 데이터 삽입 완료!")
        print(f"   - 사용자 {len(sample_users)}명 추가")
        print(f"   - 게시글 {len(sample_posts)}개 추가")
        
        return True
        
    except Exception as e:
        print(f"❌ 샘플 데이터 삽입 실패: {e}")
        if 'db' in locals():
            db.rollback()
            db.close()
        return False

def view_sample_data():
    """삽입된 샘플 데이터를 조회하는 함수"""
    print("\n👀 샘플 데이터 조회 중...")
    
    try:
        from sqlalchemy.orm import sessionmaker
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 사용자 데이터 조회
        users = db.query(User).all()
        print("\n👥 사용자 목록:")
        for user in users:
            status = "활성" if user.is_active else "비활성"
            print(f"   ID: {user.id} | {user.username} ({user.full_name}) | {user.email} | {status}")
        
        # 게시글 데이터 조회
        posts = db.query(Post).all()
        print("\n📰 게시글 목록:")
        for post in posts:
            status = "발행됨" if post.is_published else "임시저장"
            print(f"   ID: {post.id} | {post.title} | 작성자 ID: {post.author_id} | {status}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 데이터 조회 실패: {e}")
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    print("🏗️  MariaDB 테이블 생성 및 관리 도구")
    print("=" * 50)
    
    # 1단계: 테이블 생성
    if create_tables():
        # 2단계: 테이블 구조 확인
        check_tables()
        
        # 3단계: 샘플 데이터 삽입 여부 확인
        response = input("\n샘플 데이터를 삽입하시겠습니까? (y/N): ")
        if response.lower() in ['y', 'yes']:
            if insert_sample_data():
                view_sample_data()
        
        print("\n🎉 테이블 생성 및 설정 완료!")
        print("이제 FastAPI 애플리케이션에서 이 테이블들을 사용할 수 있습니다.")
        
    else:
        print("\n❌ 테이블 생성에 실패했습니다.")
        print("database.py 파일과 MariaDB 연결을 확인해주세요.")
