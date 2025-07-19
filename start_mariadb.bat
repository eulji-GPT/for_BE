#!/bin/bash

# 을지대학교 을GPT - MariaDB 실행 스크립트

echo "==============================================="
echo "🏥 을지대학교 을GPT MariaDB 환경 시작"
echo "==============================================="

# Docker가 설치되어 있는지 확인
if ! command -v docker &> /dev/null
then
    echo "❌ Docker가 설치되어 있지 않습니다."
    echo "Docker Desktop을 설치한 후 다시 시도해주세요."
    echo "다운로드: https://www.docker.com/products/docker-desktop"
    pause
    exit 1
fi

# Docker가 실행 중인지 확인
if ! docker info &> /dev/null
then
    echo "❌ Docker가 실행되지 않았습니다."
    echo "Docker Desktop을 실행한 후 다시 시도해주세요."
    pause
    exit 1
fi

echo "✅ Docker 환경 확인 완료"

# 기존 컨테이너 정리 (선택사항)
echo ""
read -p "기존 MariaDB 컨테이너를 정리하시겠습니까? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "🧹 기존 컨테이너 정리 중..."
    docker-compose -f docker-compose.mariadb.yml down -v
    echo "✅ 기존 컨테이너 정리 완료"
fi

echo ""
echo "🚀 을지대학교 을GPT MariaDB 시작 중..."
echo "이 작업은 첫 실행 시 몇 분 정도 소요될 수 있습니다."

# MariaDB 컨테이너 실행
docker-compose -f docker-compose.mariadb.yml up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ MariaDB 컨테이너가 성공적으로 시작되었습니다!"
    echo ""
    echo "📊 연결 정보:"
    echo "  • 데이터베이스: eulji_gpt_db"
    echo "  • 호스트: localhost"
    echo "  • 포트: 3306"
    echo "  • 사용자: eulji_user"
    echo "  • 비밀번호: eulji_password"
    echo ""
    echo "🔧 관리 도구:"
    echo "  • phpMyAdmin: http://localhost:8080"
    echo "  • 사용자: root"
    echo "  • 비밀번호: eulji_root_2024"
    echo ""
    echo "📝 다음 단계:"
    echo "  1. MariaDB 연결 테스트: python database.py"
    echo "  2. 샘플 데이터 생성: python setup_mariadb.py"
    echo "  3. 서버 실행: uvicorn main:app --reload"
    echo ""
    
    # MariaDB 준비 대기
    echo "⏳ MariaDB 초기화 대기 중..."
    sleep 10
    
    # 연결 테스트
    echo "🔍 MariaDB 연결 테스트..."
    if docker exec eulji-gpt-mariadb mysql -u eulji_user -peulji_password -e "SELECT 1;" eulji_gpt_db &> /dev/null
    then
        echo "✅ MariaDB 연결 테스트 성공!"
        echo ""
        echo "🎉 을지대학교 을GPT MariaDB 환경이 준비되었습니다!"
    else
        echo "⚠️  MariaDB가 아직 초기화 중입니다."
        echo "잠시 후 다시 연결 테스트를 해보세요."
    fi
    
else
    echo "❌ MariaDB 컨테이너 시작에 실패했습니다."
    echo "다음 명령어로 로그를 확인해보세요:"
    echo "docker-compose -f docker-compose.mariadb.yml logs"
fi

echo ""
echo "==============================================="
pause
