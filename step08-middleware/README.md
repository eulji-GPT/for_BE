# Step 08: 미들웨어

을지대학교 을GPT - FastAPI 미들웨어를 사용하여 요청/응답 처리를 커스터마이징하는 방법을 학습합니다.

## 🎯 학습 목표

- 을지대학교 을GPT 프로젝트에서 커스텀 미들웨어 작성
- CORS 설정 및 관리
- 로깅 미들웨어 구현
- 성능 모니터링 미들웨어

## 📋 단계별 진행

### 1. 미들웨어 기본 개념

- 요청 전/후 처리
- 미들웨어 체인
- 순서의 중요성

## 🏥 을지대학교 을GPT 미들웨어 특성

### 1. 을지대학교 을GPT 로깅 미들웨어
- 을지대학교 학생 API 접근 로그
- 을지대학교 을GPT 프로젝트 활동 추적
- 의료 데이터 접근 보안 로그

### 2. 을지대학교 을GPT 성능 모니터링
- API 응답 시간 측정
- 을지대학교 을GPT 서버 리소스 모니터링
- 데이터베이스 쿼리 성능 추적

## 🔧 을지대학교 을GPT 미들웨어 예제

### 1. 을지대학교 을GPT 커스텀 로깅
```python
@app.middleware("http")
async def eulji_gpt_logging_middleware(request: Request, call_next):
    # 을지대학교 을GPT 요청 로깅
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"을지대학교 을GPT - {request.method} {request.url} - {process_time:.4f}s")
    return response
```

- CORSMiddleware
- TrustedHostMiddleware
- GZipMiddleware

### 3. 커스텀 미들웨어

- 로깅 미들웨어
- 인증 미들웨어
- 에러 핸들링 미들웨어

## 🔧 실습

1. 다양한 미들웨어를 테스트해보세요
2. 커스텀 미들웨어를 작성해보세요
3. 미들웨어 순서를 변경해보며 동작을 확인하세요

## 📚 새로운 개념

- **미들웨어**: 요청/응답 처리 중간 계층
- **CORS**: Cross-Origin Resource Sharing
- **로깅**: 애플리케이션 활동 기록
- **성능 모니터링**: 응답 시간 및 리소스 사용량 측정

## ✅ 다음 단계

미들웨어를 익혔다면 Step 09로 이동하여 파일 업로드를 학습하세요.
