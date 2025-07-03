# Step 01: 기본 설정

이 단계에서는 FastAPI 개발을 위한 기본 환경을 설정합니다.

## 🎯 학습 목표

- Python 아나콘다 환경 설정 및 활성화
- FastAPI 및 필요한 패키지 설치
- 기본 프로젝트 구조 이해
- 개발 환경 설정 및 애플리케이션 실행

## 📋 단계별 진행

### 1. 아나콘다 환경 설정

```bash
# 사용 가능한 conda 환경 확인
conda info --envs

# 특정 환경 활성화 (예: Python3.11-eulGPT-Backend)
conda activate Python3.11-eulGPT-Backend
```

### 2. 패키지 설치

requirements.txt에 정의된 패키지들:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
```

패키지 설치:
```bash
# requirements.txt 파일의 패키지 설치
pip install -r requirements.txt

# 또는 개별 설치
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 python-multipart==0.0.6
```

### 3. 애플리케이션 실행

```bash
# 프로젝트 디렉토리로 이동
cd step01-basic-setup

# FastAPI 애플리케이션 실행
python main.py
```

실행 성공 시 다음과 같은 메시지가 표시됩니다:
```
INFO:     Started server process [프로세스ID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 4. 기본 프로젝트 구조

```
step01-basic-setup/
├── main.py          # 메인 애플리케이션 파일
├── requirements.txt # 의존성 패키지 목록
└── README.md       # 이 파일
```

## 🔧 실습

1. 아나콘다 환경을 확인하고 활성화하세요
2. 필요한 패키지가 설치되어 있는지 확인하세요
3. main.py 파일을 실행해보세요
4. 웹 브라우저에서 애플리케이션 동작을 확인하세요

## 🌐 애플리케이션 확인 방법

### 1. 웹 브라우저에서 확인
- 메인 페이지: `http://localhost:8000`
- 예상 응답: `{"message": "Hello World from FastAPI Step 01!"}`

### 2. API 문서 확인
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. 터미널에서 확인
```bash
# PowerShell에서 API 호출
Invoke-RestMethod -Uri "http://localhost:8000" -Method GET

# 또는 curl 사용 (설치된 경우)
curl http://localhost:8000
```

## 🐛 자주 발생하는 이슈

### 1. 파비콘 404 에러
```
INFO: 127.0.0.1:50120 - "GET /favicon.ico HTTP/1.1" 404 Not Found
```
- **이것은 정상입니다!** 브라우저가 자동으로 파비콘을 요청하기 때문입니다.
- 실제 API 기능에는 영향이 없습니다.

### 2. 모듈을 찾을 수 없는 에러
```
ModuleNotFoundError: No module named 'fastapi'
```
- 올바른 아나콘다 환경이 활성화되어 있는지 확인하세요.
- `conda activate Python3.11-eulGPT-Backend`

### 3. 포트 사용 중 에러
- 이미 8000 포트를 사용 중인 프로세스가 있을 수 있습니다.
- 다른 포트를 사용하거나 기존 프로세스를 종료하세요.

## 📚 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Anaconda 환경 관리](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [Uvicorn 문서](https://www.uvicorn.org/)

## ✅ 다음 단계

기본 설정이 완료되고 애플리케이션이 정상적으로 실행되면 Step 02로 이동하여 첫 번째 API를 만들어보세요.

**성공 확인 체크리스트:**
- [ ] 아나콘다 환경 활성화 완료
- [ ] FastAPI 서버 실행 성공
- [ ] `http://localhost:8000`에서 응답 확인
- [ ] `http://localhost:8000/docs`에서 API 문서 확인
