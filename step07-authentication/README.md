# Step 07: 인증

을지대학교 을GPT - JWT 토큰을 사용한 사용자 인증 시스템을 구현합니다.

## 🎯 학습 목표

- 을지대학교 을GPT 프로젝트에서 JWT 토큰 기반 인증 구현
- 비밀번호 해싱 및 검증
- 보호된 엔드포인트 생성
- 사용자 권한 관리

## 📋 단계별 진행

### 1. 패키지 설치

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

## 🏥 을지대학교 을GPT 인증 특성

### 1. 을지대학교 학생 인증
- 을지대학교 학번 기반 인증
- 전공별 권한 관리 (간호학과, 방사선학과, 의료IT학과)
- 학년별 접근 권한 설정

### 2. 을지대학교 을GPT 프로젝트 권한
- 프로젝트 팀장/팀원 권한 구분
- 을지대학교 교수/조교 관리자 권한
- AI 프로젝트 접근 권한 관리

## 🔧 을지대학교 을GPT 인증 예제

### 1. 을지대학교 학생 로그인
```python
@app.post("/auth/student-login")
def eulji_student_login(student_credentials: EuljiStudentLogin):
    # 을지대학교 학생 인증 로직
    pass
```

### 2. 을지대학교 을GPT JWT 토큰 생성
```python
def create_eulji_access_token(student_data: dict):
    # 을지대학교 을GPT 전용 JWT 토큰 생성
    pass
```

- 액세스 토큰 생성
- 토큰 검증 및 디코딩
- 토큰 만료 처리

### 3. 비밀번호 보안

- bcrypt를 사용한 해싱
- 비밀번호 검증
- 안전한 비밀번호 정책

### 4. 인증 미들웨어

- 토큰 기반 인증 의존성
- 사용자 식별
- 권한 확인

## 🔧 실습

1. 사용자 회원가입과 로그인을 테스트해보세요
2. 보호된 엔드포인트에 접근해보세요
3. 토큰 만료 상황을 테스트해보세요

## 📚 새로운 개념

- **JWT**: JSON Web Token
- **해싱**: 비밀번호 암호화
- **토큰**: 인증 정보를 담은 문자열
- **미들웨어**: 요청/응답 처리 중간 단계

## ✅ 다음 단계

인증 시스템을 익혔다면 Step 08로 이동하여 미들웨어를 학습하세요.
