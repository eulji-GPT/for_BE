# 을지대학교 을GPT - MariaDB 연결 및 실습
import pymysql
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class EuljiMariaDBConnection:
    """을지대학교 을GPT - MariaDB 연결 클래스"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'eulji_gpt_db')
        self.connection = None
        
    def connect_pymysql(self):
        """을지대학교 을GPT - PyMySQL을 사용한 MariaDB 연결"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            print("✅ PyMySQL을 사용하여 MariaDB에 성공적으로 연결되었습니다.")
            return self.connection
        except pymysql.Error as e:
            print(f"❌ PyMySQL 연결 오류: {e}")
            return None
    
    def connect_mysql_connector(self):
        """mysql-connector-python을 사용한 MariaDB 연결"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            print("✅ mysql-connector-python을 사용하여 MariaDB에 성공적으로 연결되었습니다.")
            return self.connection
        except Error as e:
            print(f"❌ mysql-connector 연결 오류: {e}")
            return None
    
    def close_connection(self):
        """연결 종료"""
        if self.connection:
            self.connection.close()
            print("🔐 데이터베이스 연결이 종료되었습니다.")

def create_sample_table(connection):
    """샘플 테이블 생성"""
    try:
        cursor = connection.cursor()
        
        # 테이블 생성 SQL
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            age INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_sql)
        connection.commit()
        print("✅ 'users' 테이블이 성공적으로 생성되었습니다.")
        
    except Exception as e:
        print(f"❌ 테이블 생성 오류: {e}")
    finally:
        cursor.close()

def insert_sample_data(connection):
    """샘플 데이터 삽입"""
    try:
        cursor = connection.cursor()
        
        # 샘플 데이터
        sample_users = [
            ('김철수', 'kimcs@example.com', 25),
            ('이영희', 'leeyh@example.com', 30),
            ('박민수', 'parkms@example.com', 28),
            ('정수진', 'jungsj@example.com', 22)
        ]
        
        # 데이터 삽입
        insert_sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
        cursor.executemany(insert_sql, sample_users)
        connection.commit()
        print(f"✅ {cursor.rowcount}개의 사용자 데이터가 성공적으로 삽입되었습니다.")
        
    except Exception as e:
        print(f"❌ 데이터 삽입 오류: {e}")
    finally:
        cursor.close()

def fetch_all_users(connection):
    """모든 사용자 조회"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        print("\n📋 모든 사용자 목록:")
        print("-" * 60)
        for user in users:
            print(f"ID: {user[0]}, 이름: {user[1]}, 이메일: {user[2]}, 나이: {user[3]}, 생성일: {user[4]}")
        
        return users
        
    except Exception as e:
        print(f"❌ 데이터 조회 오류: {e}")
    finally:
        cursor.close()

def update_user_age(connection, user_id, new_age):
    """사용자 나이 업데이트"""
    try:
        cursor = connection.cursor()
        update_sql = "UPDATE users SET age = %s WHERE id = %s"
        cursor.execute(update_sql, (new_age, user_id))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"✅ 사용자 ID {user_id}의 나이가 {new_age}로 업데이트되었습니다.")
        else:
            print(f"⚠️ 사용자 ID {user_id}를 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"❌ 데이터 업데이트 오류: {e}")
    finally:
        cursor.close()

def delete_user(connection, user_id):
    """사용자 삭제"""
    try:
        cursor = connection.cursor()
        delete_sql = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_sql, (user_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"✅ 사용자 ID {user_id}가 성공적으로 삭제되었습니다.")
        else:
            print(f"⚠️ 사용자 ID {user_id}를 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"❌ 데이터 삭제 오류: {e}")
    finally:
        cursor.close()

def main():
    """메인 실행 함수"""
    print("🔥 MariaDB 실습을 시작합니다!")
    print("=" * 50)
    
    # MariaDB 연결 객체 생성
    db = MariaDBConnection()
    
    # 연결 방법 선택 (PyMySQL 사용)
    connection = db.connect_pymysql()
    
    if connection:
        try:
            # 1. 테이블 생성
            create_sample_table(connection)
            
            # 2. 샘플 데이터 삽입
            insert_sample_data(connection)
            
            # 3. 모든 사용자 조회
            fetch_all_users(connection)
            
            # 4. 사용자 나이 업데이트
            update_user_age(connection, 1, 26)
            
            # 5. 업데이트 후 조회
            fetch_all_users(connection)
            
            # 6. 사용자 삭제
            delete_user(connection, 4)
            
            # 7. 삭제 후 조회
            fetch_all_users(connection)
            
        finally:
            # 연결 종료
            db.close_connection()
    else:
        print("❌ 데이터베이스 연결에 실패했습니다.")

if __name__ == "__main__":
    main()
