# Step 06: CRUD 작업

을지대학교 을GPT - Create, Read, Update, Delete 작업을 체계적으로 구현하는 방법을 학습합니다.

## 🎯 학습 목표

- 을지대학교 을GPT 프로젝트에서 CRUD 패턴 이해 및 구현
- 복잡한 쿼리 작성
- 데이터베이스 관계 처리
- 에러 처리 및 예외 상황 관리

## 🏥 을지대학교 을GPT 프로젝트 특성

### 1. 을지대학교 학생 데이터 CRUD
- 을지대학교 학생 정보 생성, 조회, 수정, 삭제
- 전공별(간호학과, 방사선학과, 의료IT학과) 학생 관리
- 학년별 학생 데이터 처리

### 2. 을지대학교 을GPT 프로젝트 CRUD
- AI 프로젝트, 웹개발, 모바일앱, 의료시스템 프로젝트 관리
- 프로젝트 팀 구성 및 관리
- 프로젝트 상태 추적 (진행중, 완료, 계획중)

## 🔧 을지대학교 을GPT 실습 예제

### 1. 을지대학교 학생 생성
```python
@app.post("/students/")
def create_eulji_student(student: EuljiStudentCreate, db: Session = Depends(get_db)):
    # 을지대학교 학생 데이터 생성 로직
    pass
```

### 2. 을지대학교 전공별 학생 조회
```python
@app.get("/students/major/{major}")
def get_students_by_major(major: EuljiMajor, db: Session = Depends(get_db)):
    # 전공별 을지대학교 학생 조회 로직
    pass
```

### 2. 고급 쿼리

- 필터링과 정렬
- 페이지네이션
- 검색 기능
- 집계 함수

### 3. 관계형 데이터

- 외래 키 관계
- 조인 쿼리
- 관련 데이터 로딩

## 🔧 실습

1. 다양한 CRUD 작업을 테스트해보세요
2. 복잡한 쿼리를 작성해보세요
3. 에러 상황을 시뮬레이션해보세요

## 📚 새로운 개념

- **Repository 패턴**: 데이터 액세스 로직 분리
- **쿼리 최적화**: 효율적인 데이터베이스 쿼리
- **트랜잭션 관리**: 데이터 일관성 보장
- **관계형 데이터**: 테이블 간의 연관성

## ✅ 다음 단계

CRUD 작업을 익혔다면 Step 07로 이동하여 인증 시스템을 학습하세요.
