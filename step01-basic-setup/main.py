"""
Step 01: 기본 설정
FastAPI 애플리케이션의 기본 구조를 보여주는 예제입니다.
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="FastAPI 튜토리얼 - Step 01",
    description="기본 설정 단계에서 생성된 FastAPI 애플리케이션",
    version="1.0.0"
)

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    """
    기본 루트 경로
    애플리케이션이 정상적으로 실행되는지 확인하는 엔드포인트
    """
    return {"message": "Hello World from FastAPI Step 01!"}

# 파비콘 엔드포인트 (선택사항)
@app.get("/favicon.ico")
def favicon():
    """
    파비콘 요청 처리 - 브라우저의 자동 요청을 처리합니다
    """
    return {"message": "No favicon available"}

# 서버 실행 코드 (개발용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
