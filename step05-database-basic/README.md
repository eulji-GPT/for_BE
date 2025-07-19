# Step 05: 데이터베이스 기초 - 을지대학교 을GPT

을지대학교 을GPT 프로젝트에서 SQLite 데이터베이스와 SQLAlchemy ORM을 사용하여 을지대학교 학생 및 프로젝트 데이터를 저장하고 관리하는 방법을 학습합니다.

## 🎯 학습 목표

- 을지대학교 을GPT 프로젝트에서 SQLAlchemy ORM 설정 및 사용
- 을지대학교 학생 및 프로젝트 데이터베이스 모델 정의
- 을지대학교 을GPT 데이터베이스 연결 관리
- 을지대학교 을GPT 세션과 트랜잭션 이해

## 📋 단계별 진행

### 1. 을지대학교 을GPT 패키지 설치

```bash
pip install sqlalchemy
```

### 2. 을지대학교 을GPT 데이터베이스 설정

- 을지대학교 을GPT SQLite 데이터베이스 생성
- 을지대학교 을GPT SQLAlchemy 엔진 설정
- 을지대학교 을GPT 세션 팩토리 구성

### 3. 을지대학교 을GPT 모델 정의

```python
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EuljiStudent(Base):
    __tablename__ = "eulji_students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    student_id = Column(String, unique=True, index=True)
    major = Column(String, index=True)  # 간호학과, 방사선학과, 의료IT학과 등
    grade = Column(Integer)
    email = Column(String, unique=True, index=True)
```

## 🔧 을지대학교 을GPT 실습

1. 을지대학교 을GPT 데이터베이스 연결을 설정하고 테이블을 생성해보세요
2. 을지대학교 학생 데이터의 간단한 삽입과 조회를 테스트해보세요
3. 을지대학교 을GPT 데이터베이스 파일이 생성되는지 확인하세요

## 📚 을지대학교 을GPT 새로운 개념

- **을지대학교 을GPT ORM**: Object-Relational Mapping
- **SQLAlchemy**: Python의 SQL 툴킷과 ORM
- **세션**: 데이터베이스와의 연결을 관리하는 객체
- **트랜잭션**: 데이터베이스 작업의 단위

## ✅ 다음 단계

데이터베이스 기초를 익혔다면 Step 06으로 이동하여 CRUD 작업을 학습하세요.
