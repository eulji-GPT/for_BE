# Step 06: CRUD 작업 (MariaDB 연동)

을지대학교 을GPT - Create, Read, Update, Delete 작업을 체계적으로 구현하는 방법을 학습합니다. **MariaDB 데이터베이스와 연동되어 실제 운영 환경과 유사한 환경에서 실습할 수 있습니다.**

## 🎯 학습 목표

- 을지대학교 을GPT 프로젝트에서 CRUD 패턴 이해 및 구현
- **MariaDB 데이터베이스 연동 및 관리**
- 복잡한 쿼리 작성 및 관계형 데이터베이스 활용
- 데이터베이스 관계 처리 및 성능 최적화
- 에러 처리 및 예외 상황 관리

## 🏥 을지대학교 을GPT 프로젝트 특성

### 1. 을지대학교 학생 데이터 CRUD
- 을지대학교 학생 정보 생성, 조회, 수정, 삭제
- **전공별(간호학과, 방사선학과, 의료IT학과) 학생 관리**
- 학년별 학생 데이터 처리 및 통계
- **MariaDB 기반 안정적인 데이터 저장**

### 2. 을지대학교 을GPT 프로젝트 CRUD
- AI 프로젝트, 웹개발, 모바일앱, 의료시스템 프로젝트 관리
- **프로젝트 팀 구성 및 관리 (team_leader, members 관계 테이블)**
- 프로젝트 상태 추적 (진행중, 완료, 계획중, 보류중)
- **MariaDB의 관계형 데이터베이스 특성을 활용한 데이터 무결성 보장**

## �️ 데이터베이스 설정

### MariaDB 연동 장점
- **고성능**: SQLite보다 뛰어난 성능과 동시성 처리
- **확장성**: 대량의 데이터와 다중 사용자 지원
- **안정성**: 트랜잭션 관리 및 데이터 무결성 보장
- **실제 운영 환경**: 실무에서 널리 사용되는 데이터베이스

### 빠른 시작
```bash
# 1. MariaDB 환경 설정
copy .env.example .env
# .env 파일에서 MariaDB 연결 정보 수정

# 2. 패키지 설치 (MariaDB 드라이버 포함)
pip install -r requirements.txt

# 3. MariaDB 연결 테스트 및 테이블 생성
python database.py

# 4. 샘플 데이터 생성 (선택사항)
python setup_mariadb.py

# 5. 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## �🔧 을지대학교 을GPT 실습 예제

### 1. 을지대학교 학생 생성 (MariaDB 연동)
```python
@app.post("/students/")
def create_eulji_student(student: EuljiStudentCreate, db: Session = Depends(get_db)):
    """
    을지대학교 학생 데이터 생성
    - MariaDB AUTO_INCREMENT로 ID 자동 생성
    - 학번 중복 체크 (UNIQUE 제약조건)
    - 트랜잭션 관리로 데이터 무결성 보장
    """
    try:
        # 학번 중복 체크 (MariaDB UNIQUE 인덱스 활용)
        existing_student = db.query(EuljiStudent).filter(
            EuljiStudent.student_number == student.student_number
        ).first()
        if existing_student:
            raise HTTPException(status_code=400, detail="이미 존재하는 학번입니다.")
        
        db_student = EuljiStudent(**student.dict())
        db.add(db_student)
        db.commit()  # MariaDB 트랜잭션 커밋
        db.refresh(db_student)  # AUTO_INCREMENT ID 반영
        
        return db_student
        
    except Exception as e:
        db.rollback()  # MariaDB 트랜잭션 롤백
        raise HTTPException(status_code=500, detail="학생 생성에 실패했습니다.")
```

### 2. 을지대학교 전공별 학생 조회 (MariaDB 인덱스 활용)
```python
@app.get("/students/major/{major}")
def get_students_by_major(major: EuljiMajor, db: Session = Depends(get_db)):
    """
    전공별 을지대학교 학생 조회
    - MariaDB 인덱스를 활용한 빠른 검색
    - ENUM 타입을 통한 데이터 무결성
    """
    students = db.query(EuljiStudent).filter(EuljiStudent.major == major).all()
    return students
```

### 3. 고급 쿼리 및 통계 (MariaDB 집계 함수 활용)
```python
@app.get("/stats/students-by-major")
def get_students_stats_by_major(db: Session = Depends(get_db)):
    """
    전공별 학생 수 통계
    - MariaDB GROUP BY 및 COUNT 함수 활용
    - 효율적인 집계 쿼리
    """
    from sqlalchemy import func
    
    stats = db.query(
        EuljiStudent.major,
        func.count(EuljiStudent.id).label('student_count')
    ).group_by(EuljiStudent.major).all()
    
    return {major: count for major, count in stats}
```

## 📊 데이터베이스 스키마 (MariaDB)

### 주요 테이블
1. **eulji_students** - 을지대학교 학생 정보
   - AUTO_INCREMENT PRIMARY KEY
   - UNIQUE INDEX (student_number, email)
   - INDEX (major, grade) - 빠른 검색을 위한 복합 인덱스

2. **eulji_projects** - 을지대학교 을GPT 프로젝트
   - FOREIGN KEY (team_leader_id) REFERENCES eulji_students(id)
   - INDEX (status, category) - 상태 및 카테고리별 검색

3. **project_members** - 프로젝트 멤버 관계
   - 다대다 관계 구현
   - FOREIGN KEY 제약조건으로 참조 무결성 보장

### MariaDB 특화 기능
- **트랜잭션 관리**: ACID 특성 보장
- **인덱스 최적화**: B-Tree 인덱스를 통한 빠른 검색
- **외래키 제약**: 참조 무결성 자동 관리
- **한글 지원**: utf8mb4 문자셋으로 한글 완벽 지원

## 🔧 실습 과제

### 기본 과제
1. **MariaDB 연결 설정**: 로컬 또는 Docker MariaDB와 연결
2. **CRUD 작업 테스트**: 각 엔드포인트에서 데이터 생성, 조회, 수정, 삭제
3. **트랜잭션 테스트**: 오류 상황에서 롤백 동작 확인

### 심화 과제
1. **복잡한 쿼리 작성**: JOIN을 활용한 프로젝트-학생 관계 조회
2. **성능 최적화**: EXPLAIN을 사용한 쿼리 실행 계획 분석
3. **데이터 백업**: mysqldump를 사용한 데이터 백업 및 복원
4. **인덱스 최적화**: 자주 조회되는 컬럼에 인덱스 추가

## 📚 새로운 개념

### MariaDB 관련
- **MySQL 호환성**: MySQL과 완벽 호환되는 오픈소스 데이터베이스
- **스토리지 엔진**: InnoDB를 통한 트랜잭션 및 외래키 지원
- **연결 풀링**: SQLAlchemy의 연결 풀을 통한 효율적인 연결 관리
- **문자셋 설정**: utf8mb4를 통한 한글 및 이모지 완벽 지원

### CRUD 패턴
- **Repository 패턴**: 데이터 액세스 로직 분리 및 재사용성 향상
- **쿼리 최적화**: N+1 문제 방지 및 지연 로딩 활용
- **트랜잭션 관리**: 데이터 일관성 보장 및 동시성 처리
- **관계형 데이터**: 외래키와 조인을 통한 정규화된 데이터 관리

## 🚀 배포 및 운영

### 개발 환경
```bash
# 로컬 MariaDB 사용
MARIADB_HOST=localhost
MARIADB_PORT=3306
MARIADB_DATABASE=eulji_gpt_db
```

### 운영 환경
```bash
# 클라우드 MariaDB 또는 별도 서버 사용
MARIADB_HOST=db.eulji.ac.kr
MARIADB_PORT=3306
MARIADB_DATABASE=eulji_gpt_production
```

## 📈 성능 모니터링

### 쿼리 성능 분석
```sql
-- 느린 쿼리 로그 활성화
SET GLOBAL slow_query_log = 1;
SET GLOBAL long_query_time = 1;

-- 실행 계획 확인
EXPLAIN SELECT * FROM eulji_students WHERE major = '간호학과';
```

### 인덱스 사용률 확인
```sql
-- 인덱스 통계 확인
SHOW INDEX FROM eulji_students;

-- 테이블 상태 확인
SHOW TABLE STATUS LIKE 'eulji_students';
```

## 📖 참고 문서

- [MARIADB_SETUP.md](./MARIADB_SETUP.md) - 자세한 MariaDB 설정 가이드
- [FastAPI Database Documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [MariaDB Documentation](https://mariadb.com/kb/)

## ✅ 다음 단계

CRUD 작업과 MariaDB 연동을 익혔다면 Step 07로 이동하여 JWT 인증 시스템을 학습하세요. 인증 시스템에서도 MariaDB를 활용한 사용자 관리를 다룹니다.

---

**💡 팁**: MariaDB 연동을 통해 실제 운영 환경과 유사한 데이터베이스 경험을 쌓을 수 있습니다. 트랜잭션 관리, 인덱스 최적화, 쿼리 튜닝 등 실무에서 중요한 기술들을 함께 익혀보세요!

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
