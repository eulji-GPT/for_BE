#!/usr/bin/env python3
"""
MariaDB 연결 테스트 스크립트
실제 데이터베이스 연결 전에 간단한 테스트를 수행합니다.
"""

import pymysql
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def test_connection():
    """데이터베이스 연결 테스트"""
    
    # 연결 정보
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'test_db')
    }
    
    print("🔍 MariaDB 연결 테스트를 시작합니다...")
    print(f"서버: {config['host']}:{config['port']}")
    print(f"사용자: {config['user']}")
    print(f"데이터베이스: {config['database']}")
    print("-" * 50)
    
    # PyMySQL 테스트
    print("\n1️⃣ PyMySQL 연결 테스트")
    try:
        connection = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ PyMySQL 연결 성공!")
        print(f"   MariaDB 버전: {version[0]}")
        
        # 간단한 쿼리 테스트
        cursor.execute("SELECT 1 + 1 AS result")
        result = cursor.fetchone()
        print(f"   테스트 쿼리 결과: {result[0]}")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ PyMySQL 연결 실패: {e}")
    
    # mysql-connector-python 테스트
    print("\n2️⃣ mysql-connector-python 연결 테스트")
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ mysql-connector-python 연결 성공!")
        print(f"   MariaDB 버전: {version[0]}")
        
        # 간단한 쿼리 테스트
        cursor.execute("SELECT 2 + 2 AS result")
        result = cursor.fetchone()
        print(f"   테스트 쿼리 결과: {result[0]}")
        
        connection.close()
        
    except Error as e:
        print(f"❌ mysql-connector-python 연결 실패: {e}")
    
    print("\n🎉 연결 테스트 완료!")

def check_environment():
    """환경 설정 확인"""
    print("\n🔧 환경 설정 확인")
    print("-" * 30)
    
    # .env 파일 존재 확인
    if os.path.exists('.env'):
        print("✅ .env 파일 존재")
    else:
        print("⚠️  .env 파일이 없습니다. .env.example을 참고하여 생성하세요.")
    
    # 환경 변수 확인
    required_vars = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'DB_PASSWORD':
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: 설정되지 않음")

def main():
    """메인 실행 함수"""
    print("🚀 MariaDB 연결 테스트 스크립트")
    print("=" * 40)
    
    # 환경 설정 확인
    check_environment()
    
    # 연결 테스트
    test_connection()
    
    print("\n💡 팁:")
    print("- 연결에 실패하면 MariaDB 서비스 상태를 확인하세요")
    print("- .env 파일의 연결 정보를 확인하세요")
    print("- 방화벽 설정을 확인하세요")

if __name__ == "__main__":
    main()
