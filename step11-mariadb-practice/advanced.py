import pymysql
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class MariaDBAdvanced:
    """고급 MariaDB 기능 실습"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'test_db')
        self.connection = None
        
    def connect(self):
        """MariaDB 연결"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            print("✅ MariaDB 연결 성공")
            return self.connection
        except pymysql.Error as e:
            print(f"❌ 연결 오류: {e}")
            return None
    
    def create_advanced_tables(self):
        """고급 테이블 생성 (외래키, 인덱스 포함)"""
        try:
            cursor = self.connection.cursor()
            
            # 카테고리 테이블
            create_categories_sql = """
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # 제품 테이블 (외래키 포함)
            create_products_sql = """
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                category_id INT,
                stock_quantity INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
                INDEX idx_category_id (category_id),
                INDEX idx_price (price)
            )
            """
            
            # 주문 테이블
            create_orders_sql = """
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                product_id INT,
                quantity INT NOT NULL,
                total_price DECIMAL(10, 2) NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_order_date (order_date)
            )
            """
            
            cursor.execute(create_categories_sql)
            cursor.execute(create_products_sql)
            cursor.execute(create_orders_sql)
            self.connection.commit()
            print("✅ 고급 테이블들이 성공적으로 생성되었습니다.")
            
        except Exception as e:
            print(f"❌ 테이블 생성 오류: {e}")
        finally:
            cursor.close()
    
    def insert_sample_data(self):
        """샘플 데이터 삽입"""
        try:
            cursor = self.connection.cursor()
            
            # 카테고리 데이터
            categories = [
                ('전자제품', '전자기기 및 액세서리'),
                ('의류', '남녀 의류 및 패션 아이템'),
                ('도서', '각종 서적 및 교재'),
                ('가구', '생활용품 및 가구')
            ]
            
            cursor.executemany(
                "INSERT INTO categories (name, description) VALUES (%s, %s)",
                categories
            )
            
            # 제품 데이터
            products = [
                ('노트북', '고성능 게이밍 노트북', 1500000, 1, 10),
                ('스마트폰', '최신 스마트폰', 800000, 1, 25),
                ('청바지', '편안한 청바지', 50000, 2, 30),
                ('파이썬 책', '파이썬 프로그래밍 가이드', 25000, 3, 15),
                ('책상', '컴퓨터 책상', 200000, 4, 5)
            ]
            
            cursor.executemany(
                "INSERT INTO products (name, description, price, category_id, stock_quantity) VALUES (%s, %s, %s, %s, %s)",
                products
            )
            
            # 주문 데이터
            orders = [
                (1, 1, 1, 1500000),
                (2, 2, 2, 1600000),
                (1, 3, 3, 150000),
                (3, 4, 1, 25000)
            ]
            
            cursor.executemany(
                "INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
                orders
            )
            
            self.connection.commit()
            print("✅ 샘플 데이터가 성공적으로 삽입되었습니다.")
            
        except Exception as e:
            print(f"❌ 데이터 삽입 오류: {e}")
        finally:
            cursor.close()
    
    def complex_queries(self):
        """복잡한 쿼리 실행"""
        try:
            cursor = self.connection.cursor()
            
            # JOIN 쿼리
            print("\n🔍 JOIN 쿼리 - 사용자별 주문 정보:")
            join_sql = """
            SELECT u.name, p.name, o.quantity, o.total_price, o.order_date
            FROM users u
            JOIN orders o ON u.id = o.user_id
            JOIN products p ON o.product_id = p.id
            ORDER BY o.order_date DESC
            """
            
            cursor.execute(join_sql)
            results = cursor.fetchall()
            for row in results:
                print(f"사용자: {row[0]}, 상품: {row[1]}, 수량: {row[2]}, 가격: {row[3]}, 주문일: {row[4]}")
            
            # 그룹화 쿼리
            print("\n📊 그룹화 쿼리 - 카테고리별 상품 수 및 평균 가격:")
            group_sql = """
            SELECT c.name, COUNT(p.id) as product_count, AVG(p.price) as avg_price
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.id, c.name
            ORDER BY product_count DESC
            """
            
            cursor.execute(group_sql)
            results = cursor.fetchall()
            for row in results:
                print(f"카테고리: {row[0]}, 상품 수: {row[1]}, 평균 가격: {row[2]:.2f}")
            
            # 서브쿼리
            print("\n🎯 서브쿼리 - 평균 가격보다 비싼 상품:")
            subquery_sql = """
            SELECT name, price
            FROM products
            WHERE price > (SELECT AVG(price) FROM products)
            ORDER BY price DESC
            """
            
            cursor.execute(subquery_sql)
            results = cursor.fetchall()
            for row in results:
                print(f"상품: {row[0]}, 가격: {row[1]}")
            
        except Exception as e:
            print(f"❌ 쿼리 실행 오류: {e}")
        finally:
            cursor.close()
    
    def transaction_example(self):
        """트랜잭션 예제"""
        try:
            cursor = self.connection.cursor()
            
            # 트랜잭션 시작
            self.connection.begin()
            
            # 재고 감소
            cursor.execute("UPDATE products SET stock_quantity = stock_quantity - 1 WHERE id = 1")
            
            # 주문 추가
            cursor.execute(
                "INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (1, 1, 1, 1500000)"
            )
            
            # 커밋
            self.connection.commit()
            print("✅ 트랜잭션이 성공적으로 처리되었습니다.")
            
        except Exception as e:
            # 롤백
            self.connection.rollback()
            print(f"❌ 트랜잭션 오류 (롤백됨): {e}")
        finally:
            cursor.close()
    
    def stored_procedure_example(self):
        """저장 프로시저 예제"""
        try:
            cursor = self.connection.cursor()
            
            # 저장 프로시저 생성
            create_proc_sql = """
            DROP PROCEDURE IF EXISTS GetUserOrders;
            CREATE PROCEDURE GetUserOrders(IN user_id INT)
            BEGIN
                SELECT u.name, p.name, o.quantity, o.total_price, o.order_date
                FROM users u
                JOIN orders o ON u.id = o.user_id
                JOIN products p ON o.product_id = p.id
                WHERE u.id = user_id;
            END
            """
            
            cursor.execute(create_proc_sql)
            self.connection.commit()
            
            # 저장 프로시저 실행
            cursor.callproc('GetUserOrders', [1])
            
            for result in cursor.stored_results():
                rows = result.fetchall()
                print("\n📋 저장 프로시저 결과:")
                for row in rows:
                    print(f"사용자: {row[0]}, 상품: {row[1]}, 수량: {row[2]}, 가격: {row[3]}, 주문일: {row[4]}")
            
        except Exception as e:
            print(f"❌ 저장 프로시저 오류: {e}")
        finally:
            cursor.close()
    
    def close_connection(self):
        """연결 종료"""
        if self.connection:
            self.connection.close()
            print("🔐 데이터베이스 연결이 종료되었습니다.")

def main():
    """메인 실행 함수"""
    print("🚀 MariaDB 고급 기능 실습을 시작합니다!")
    print("=" * 50)
    
    db = MariaDBAdvanced()
    
    if db.connect():
        try:
            # 1. 고급 테이블 생성
            db.create_advanced_tables()
            
            # 2. 샘플 데이터 삽입
            db.insert_sample_data()
            
            # 3. 복잡한 쿼리 실행
            db.complex_queries()
            
            # 4. 트랜잭션 예제
            db.transaction_example()
            
            # 5. 저장 프로시저 예제
            db.stored_procedure_example()
            
        finally:
            db.close_connection()
    else:
        print("❌ 데이터베이스 연결에 실패했습니다.")

if __name__ == "__main__":
    main()
