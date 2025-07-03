"""
Step 02: 첫 번째 API
다양한 HTTP 메서드와 응답 타입을 보여주는 예제입니다.
"""

from fastapi import FastAPI
from datetime import datetime

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="FastAPI 튜토리얼 - Step 02",
    description="첫 번째 API 단계 - 다양한 엔드포인트 예제",
    version="1.0.0"
)

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    """
    기본 루트 경로
    """
    return {"message": "Welcome to FastAPI Step 02!"}

# 간단한 JSON 응답
@app.get("/hello")
def say_hello():
    """
    간단한 인사말을 반환하는 엔드포인트
    """
    return {"greeting": "Hello", "message": "FastAPI로 만든 첫 번째 API입니다!"}

# 현재 시간 반환
@app.get("/time")
def get_current_time():
    """
    현재 시간을 반환하는 엔드포인트
    """
    return {
        "current_time": datetime.now().isoformat(),
        "timestamp": datetime.now().timestamp()
    }

# 서버 정보 반환
@app.get("/info")
def get_server_info():
    """
    서버 정보를 반환하는 엔드포인트
    """
    return {
        "server": "FastAPI",
        "version": "Step 02",
        "status": "running",
        "endpoints": [
            "/",
            "/hello",
            "/time",
            "/info"
        ]
    }

# POST 엔드포인트 예제
@app.post("/echo")
def echo_message(message: dict):
    """
    전달받은 메시지를 그대로 반환하는 엔드포인트
    """
    return {
        "received": message,
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }

# 계산기 엔드포인트
@app.get("/calculate/{operation}/{a}/{b}")
def calculate(operation: str, a: float, b: float):
    """
    간단한 계산을 수행하는 엔드포인트
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return {"error": "Division by zero is not allowed"}
        result = a / b
    else:
        return {"error": "Invalid operation"}
    
    return {
        "operation": operation,
        "operand1": a,
        "operand2": b,
        "result": result
    }

# 서버 실행 코드 (개발용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
