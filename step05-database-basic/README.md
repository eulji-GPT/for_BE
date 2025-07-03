# Step 05: 데이터베이스 기초

이 단계에서는 SQLite 데이터베이스와 SQLAlchemy ORM을 사용하여 데이터를 저장하고 관리하는 방법을 학습합니다.

## 🎯 학습 목표

- SQLAlchemy ORM 설정 및 사용
- 데이터베이스 모델 정의
- 데이터베이스 연결 관리
- 세션과 트랜잭션 이해

## 📋 단계별 진행

### 1. 패키지 설치

```bash
pip install sqlalchemy
```

### 2. 데이터베이스 설정

- SQLite 데이터베이스 생성
- SQLAlchemy 엔진 설정
- 세션 팩토리 구성

### 3. 모델 정의

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

## 🔧 실습

1. 데이터베이스 연결을 설정하고 테이블을 생성해보세요
2. 간단한 데이터 삽입과 조회를 테스트해보세요
3. 데이터베이스 파일이 생성되는지 확인하세요

## 📚 새로운 개념

- **ORM**: Object-Relational Mapping
- **SQLAlchemy**: Python의 SQL 툴킷과 ORM
- **세션**: 데이터베이스와의 연결을 관리하는 객체
- **트랜잭션**: 데이터베이스 작업의 단위

## ✅ 다음 단계

데이터베이스 기초를 익혔다면 Step 06으로 이동하여 CRUD 작업을 학습하세요.
