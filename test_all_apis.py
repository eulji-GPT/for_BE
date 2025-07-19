"""
을지대학교 을GPT - API 테스트 스크립트
모든 단계의 API를 테스트합니다.
"""

import requests
import json
import time
from datetime import datetime

# 각 단계별 서버 URL
SERVERS = {
    "Step06 CRUD": "http://localhost:8000",
    "Step07 인증": "http://localhost:8001", 
    "Step08 미들웨어": "http://localhost:8002",
    "Step09 파일업로드": "http://localhost:8003",
    "Step10 배포": "http://localhost:8004"
}

def test_health_check(server_name, base_url):
    """헬스체크 테스트"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ {server_name}: 정상 작동")
            return True
        else:
            print(f"❌ {server_name}: 응답 오류 (상태코드: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {server_name}: 연결 실패 - {str(e)}")
        return False

def test_root_endpoint(server_name, base_url):
    """루트 엔드포인트 테스트"""
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {server_name} 루트: {data.get('message', 'OK')}")
            return True
        else:
            print(f"❌ {server_name} 루트: 응답 오류")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {server_name} 루트: 연결 실패")
        return False

def test_step06_crud(base_url):
    """Step 06 CRUD API 테스트"""
    print("\n🔍 Step 06 CRUD 작업 테스트:")
    
    # 학생 목록 조회
    try:
        response = requests.get(f"{base_url}/students/")
        if response.status_code == 200:
            students = response.json()
            print(f"  ✅ 학생 목록 조회: {len(students)}명")
        else:
            print(f"  ❌ 학생 목록 조회 실패")
    except Exception as e:
        print(f"  ❌ 학생 목록 조회 오류: {str(e)}")
    
    # 프로젝트 목록 조회
    try:
        response = requests.get(f"{base_url}/projects/")
        if response.status_code == 200:
            projects = response.json()
            print(f"  ✅ 프로젝트 목록 조회: {len(projects)}개")
        else:
            print(f"  ❌ 프로젝트 목록 조회 실패")
    except Exception as e:
        print(f"  ❌ 프로젝트 목록 조회 오류: {str(e)}")

def test_step07_auth(base_url):
    """Step 07 인증 시스템 테스트"""
    print("\n🔐 Step 07 인증 시스템 테스트:")
    
    # 보호된 엔드포인트 접근 (토큰 없이)
    try:
        response = requests.get(f"{base_url}/auth/me")
        if response.status_code == 401:
            print(f"  ✅ 인증 보호 정상 작동 (401 Unauthorized)")
        else:
            print(f"  ❌ 인증 보호 실패")
    except Exception as e:
        print(f"  ❌ 인증 테스트 오류: {str(e)}")

def test_step08_middleware(base_url):
    """Step 08 미들웨어 테스트"""
    print("\n⚙️ Step 08 미들웨어 테스트:")
    
    # 헤더 테스트
    try:
        response = requests.get(f"{base_url}/test/headers")
        if response.status_code == 200:
            print(f"  ✅ 헤더 테스트 성공")
            # 커스텀 헤더 확인
            if 'X-University' in response.headers:
                print(f"  ✅ 커스텀 헤더 확인: {response.headers.get('X-University')}")
        else:
            print(f"  ❌ 헤더 테스트 실패")
    except Exception as e:
        print(f"  ❌ 헤더 테스트 오류: {str(e)}")

def test_step09_fileupload(base_url):
    """Step 09 파일 업로드 테스트"""
    print("\n📁 Step 09 파일 업로드 테스트:")
    
    # 파일 목록 조회
    try:
        response = requests.get(f"{base_url}/files/list")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ 파일 목록 조회: {data.get('count', 0)}개")
        else:
            print(f"  ❌ 파일 목록 조회 실패")
    except Exception as e:
        print(f"  ❌ 파일 목록 조회 오류: {str(e)}")
    
    # 업로드 통계 조회
    try:
        response = requests.get(f"{base_url}/files/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ 업로드 통계: {data.get('total_files', 0)}개 파일")
        else:
            print(f"  ❌ 업로드 통계 조회 실패")
    except Exception as e:
        print(f"  ❌ 업로드 통계 조회 오류: {str(e)}")

def test_step10_deployment(base_url):
    """Step 10 배포 테스트"""
    print("\n🚀 Step 10 배포 테스트:")
    
    # 시스템 통계 조회
    try:
        response = requests.get(f"{base_url}/api/v1/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ 시스템 통계: {data.get('university')} {data.get('project')}")
            stats = data.get('statistics', {})
            print(f"  📊 학생 수: {stats.get('total_students', 0)}명")
            print(f"  📊 프로젝트 수: {stats.get('total_projects', 0)}개")
        else:
            print(f"  ❌ 시스템 통계 조회 실패")
    except Exception as e:
        print(f"  ❌ 시스템 통계 조회 오류: {str(e)}")

def main():
    """메인 테스트 함수"""
    print("=" * 60)
    print("🏥 을지대학교 을GPT 프로젝트 API 테스트")
    print(f"📅 테스트 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 각 서버 상태 확인
    active_servers = {}
    
    for server_name, base_url in SERVERS.items():
        print(f"\n🔍 {server_name} 상태 확인...")
        
        # 헬스체크 우선 시도
        health_ok = test_health_check(server_name, base_url)
        if not health_ok:
            # 헬스체크 실패시 루트 엔드포인트 시도
            root_ok = test_root_endpoint(server_name, base_url)
            if root_ok:
                active_servers[server_name] = base_url
        else:
            active_servers[server_name] = base_url
    
    print(f"\n✅ 활성 서버: {len(active_servers)}개")
    
    # 각 단계별 상세 테스트
    if "Step06 CRUD" in active_servers:
        test_step06_crud(active_servers["Step06 CRUD"])
    
    if "Step07 인증" in active_servers:
        test_step07_auth(active_servers["Step07 인증"])
    
    if "Step08 미들웨어" in active_servers:
        test_step08_middleware(active_servers["Step08 미들웨어"])
    
    if "Step09 파일업로드" in active_servers:
        test_step09_fileupload(active_servers["Step09 파일업로드"])
    
    if "Step10 배포" in active_servers:
        test_step10_deployment(active_servers["Step10 배포"])
    
    print("\n" + "=" * 60)
    print("🎉 을지대학교 을GPT API 테스트 완료!")
    print(f"📅 테스트 종료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main()
