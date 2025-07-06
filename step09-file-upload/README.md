# Step 09: 파일 업로드

을지대학교 을GPT - 파일 업로드 기능을 구현하고 파일을 안전하게 처리하는 방법을 학습합니다.

## 🎯 학습 목표

- 을지대학교 을GPT 프로젝트에서 파일 업로드 엔드포인트 구현
- 파일 유효성 검사
- 이미지 파일 처리
- 파일 저장 및 관리

## 📋 단계별 진행

### 1. 파일 업로드 기본

- UploadFile 사용
- 파일 크기 제한
- 파일 형식 검증

## 🏥 을지대학교 을GPT 파일 업로드 특성

### 1. 을지대학교 학생 프로필 사진
- 을지대학교 학생 증명사진 업로드
- 프로필 이미지 크기 조정 및 최적화
- 을지대학교 을GPT 학생 이미지 저장소 관리

### 2. 을지대학교 을GPT 프로젝트 파일
- 프로젝트 문서 업로드 (PDF, DOC)
- 의료 이미지 파일 처리
- AI 모델 파일 업로드 및 관리

## 🔧 을지대학교 을GPT 파일 업로드 예제

### 1. 을지대학교 학생 프로필 업로드
```python
@app.post("/students/{student_id}/profile-image")
async def upload_eulji_student_profile(
    student_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 을지대학교 학생 프로필 이미지 업로드 로직
    pass
```

### 2. 을지대학교 을GPT 프로젝트 파일 업로드
```python
@app.post("/projects/{project_id}/files")
async def upload_eulji_project_file(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 을지대학교 을GPT 프로젝트 파일 업로드 로직
    pass
```

```bash
pip install Pillow
```

### 3. 파일 저장

- 로컬 파일 시스템
- 파일명 안전성
- 디렉토리 구조

### 4. 보안 고려사항

- 파일 형식 검증
- 악성 파일 차단
- 파일 크기 제한

## 🔧 실습

1. 다양한 형식의 파일을 업로드해보세요
2. 큰 파일 업로드를 테스트해보세요
3. 잘못된 파일 형식으로 테스트해보세요

## 📚 새로운 개념

- **UploadFile**: FastAPI의 파일 업로드 클래스
- **MIME 타입**: 파일 형식 식별자
- **파일 스트림**: 메모리 효율적인 파일 처리
- **이미지 처리**: Pillow를 사용한 이미지 조작

## ✅ 다음 단계

파일 업로드를 익혔다면 Step 10으로 이동하여 배포를 학습하세요.
