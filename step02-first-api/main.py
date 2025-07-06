"""
Step 02: 첫 번째 API
을지대학교 을GPT - 다양한 HTTP 메서드와 응답 타입
"""

from fastapi import FastAPI
from datetime import datetime

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="을지대학교 을GPT - Step 02",
    description="을지대학교 을GPT 프로젝트 - 첫 번째 API 단계",
    version="1.0.0"
)

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    """
    을지대학교 을GPT - 기본 루트 경로
    """
    return {"message": "을지대학교 을GPT - FastAPI Step 02!", "university": "을지대학교"}

# 을GPT 프로젝트 소개
@app.get("/hello")
def say_hello():
    """
    을지대학교 을GPT 프로젝트 소개 엔드포인트
    """
    return {
        "greeting": "안녕하세요! 을지대학교입니다", 
        "message": "을GPT 프로젝트에 오신 것을 환영합니다!",
        "project": "을지대학교 을GPT"
    }

# 현재 시간 반환
@app.get("/time")
def get_current_time():
    """
    을지대학교 을GPT - 현재 시간을 반환하는 엔드포인트
    """
    return {
        "current_time": datetime.now().isoformat(),
        "timestamp": datetime.now().timestamp(),
        "message": "을지대학교 을GPT 서버 시간"
    }

# 서버 정보 반환
@app.get("/info")
def get_server_info():
    """
    을지대학교 을GPT - 서버 정보를 반환하는 엔드포인트
    """
    return {
        "university": "을지대학교",
        "project": "을GPT",
        "server": "FastAPI",
        "version": "Step 02",
        "status": "running",
        "endpoints": [
            "/",
            "/hello",
            "/time",
            "/info",
            "/echo",
            "/calculate"
        ]
    }

# POST 엔드포인트 예제
@app.post("/echo")
def echo_message(message: dict):
    """
    을지대학교 을GPT - 전달받은 메시지를 그대로 반환하는 엔드포인트
    """
    return {
        "received": message,
        "timestamp": datetime.now().isoformat(),
        "status": "success",
        "project": "을지대학교 을GPT",
        "response_from": "을지대학교 FastAPI 서버"
    }

# 을GPT 계산기 엔드포인트
@app.get("/calculate/{operation}/{a}/{b}")
def calculate(operation: str, a: float, b: float):
    """
    을지대학교 을GPT - 간단한 계산을 수행하는 엔드포인트
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return {
                "error": "0으로 나눌 수 없습니다", 
                "message": "을지대학교 을GPT - 계산 오류"
            }
        result = a / b
    else:
        return {
            "error": "지원하지 않는 연산입니다", 
            "message": "을지대학교 을GPT - 연산 오류"
        }
    
    return {
        "operation": operation,
        "operand1": a,
        "operand2": b,
        "result": result,
        "calculated_by": "을지대학교 을GPT 계산기"
    }

# 서버 실행 코드 (개발용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
