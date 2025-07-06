"""
Step 01: 기본 설정
을지대학교 을GPT - FastAPI 애플리케이션의 기본 구조
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="을지대학교 을GPT - Step 01",
    description="을지대학교 을GPT 프로젝트의 기본 설정 단계",
    version="1.0.0"
)

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    """
    을지대학교 을GPT - 기본 루트 경로
    애플리케이션이 정상적으로 실행되는지 확인하는 엔드포인트
    """
    return {"message": "을지대학교 을GPT - FastAPI Step 01 실행 중!", "project": "을지대학교 을GPT 프로젝트"}

# 을GPT 프로젝트 정보 엔드포인트
@app.get("/project-info")
def get_project_info():
    """
    을지대학교 을GPT 프로젝트 정보를 반환하는 엔드포인트
    """
    return {
        "university": "을지대학교",
        "project_name": "을GPT",
        "description": "을지대학교 학생들을 위한 AI 기반 프로젝트",
        "step": "01 - 기본 설정",
        "status": "개발 중"
    }

# 파비콘 엔드포인트 (선택사항)
@app.get("/favicon.ico")
def favicon():
    """
    파비콘 요청 처리 - 을지대학교 을GPT 프로젝트
    """
    return {"message": "을지대학교 을GPT - 파비콘 준비 중"}

# 서버 실행 코드 (개발용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
