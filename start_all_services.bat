#!/bin/bash

# 을지대학교 을GPT - 개발 환경 실행 스크립트

echo "==============================================="
echo "을지대학교 을GPT 프로젝트 개발 환경 시작"
echo "==============================================="

# Step 06: CRUD 작업 실행
echo "📚 Step 06: CRUD 작업 시작..."
cd step06-crud-operations
echo "가상환경 생성 및 패키지 설치..."
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
echo "데이터베이스 테이블 생성..."
python database.py
echo "Step 06 서버 시작 (포트 8000)..."
start cmd /k "venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
cd ..

# Step 07: 인증 시스템 실행
echo "🔐 Step 07: 인증 시스템 시작..."
cd step07-authentication
echo "가상환경 생성 및 패키지 설치..."
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
echo "데이터베이스 테이블 생성..."
python database.py
echo "Step 07 서버 시작 (포트 8001)..."
start cmd /k "venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8001 --reload"
cd ..

# Step 08: 미들웨어 실행
echo "⚙️ Step 08: 미들웨어 시스템 시작..."
cd step08-middleware
echo "가상환경 생성 및 패키지 설치..."
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
echo "데이터베이스 테이블 생성..."
python database.py
echo "Step 08 서버 시작 (포트 8002)..."
start cmd /k "venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8002 --reload"
cd ..

# Step 09: 파일 업로드 실행
echo "📁 Step 09: 파일 업로드 시스템 시작..."
cd step09-file-upload
echo "가상환경 생성 및 패키지 설치..."
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
echo "데이터베이스 테이블 생성..."
python database.py
echo "Step 09 서버 시작 (포트 8003)..."
start cmd /k "venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8003 --reload"
cd ..

# Step 10: 배포 실행
echo "🚀 Step 10: 배포 시스템 시작..."
cd step10-deployment
echo "가상환경 생성 및 패키지 설치..."
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
echo "데이터베이스 테이블 생성..."
python database.py
echo "Step 10 서버 시작 (포트 8004)..."
start cmd /k "venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8004 --reload"
cd ..

echo "==============================================="
echo "🎉 을지대학교 을GPT 모든 서비스가 시작되었습니다!"
echo ""
echo "📋 접속 정보:"
echo "Step 06 CRUD: http://localhost:8000/docs"
echo "Step 07 인증: http://localhost:8001/docs"
echo "Step 08 미들웨어: http://localhost:8002/docs"
echo "Step 09 파일업로드: http://localhost:8003/docs"
echo "Step 10 배포: http://localhost:8004/docs"
echo ""
echo "💡 각 서비스는 별도의 CMD 창에서 실행됩니다."
echo "서비스를 종료하려면 각 CMD 창에서 Ctrl+C를 누르세요."
echo "==============================================="

pause
