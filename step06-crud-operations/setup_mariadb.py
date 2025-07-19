"""
을지대학교 을GPT - MariaDB 초기 설정 및 데이터 삽입 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal, create_tables, test_mariadb_connection
from models import EuljiStudent, EuljiProject, ProjectMember, EuljiMajor, ProjectStatus
from passlib.context import CryptContext

# 비밀번호 해싱용
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def insert_sample_data():
    """
    을지대학교 을GPT 샘플 데이터 삽입
    """
    db = SessionLocal()
    
    try:
        # 기존 데이터 확인
        existing_students = db.query(EuljiStudent).count()
        if existing_students > 0:
            print(f"이미 {existing_students}명의 학생 데이터가 존재합니다.")
            return
        
        print("을지대학교 을GPT 샘플 데이터 생성 중...")
        
        # 을지대학교 학생 샘플 데이터
        students_data = [
            {
                "name": "김간호",
                "student_number": "2024001",
                "major": EuljiMajor.NURSING,
                "grade": 3,
                "email": "nursing01@eulji.ac.kr",
                "phone": "010-1234-5678",
                "address": "대전광역시 중구 을지로"
            },
            {
                "name": "박방사",
                "student_number": "2024002",
                "major": EuljiMajor.RADIOLOGY,
                "grade": 4,
                "email": "radiology01@eulji.ac.kr",
                "phone": "010-2345-6789",
                "address": "대전광역시 중구 을지로"
            },
            {
                "name": "이의료",
                "student_number": "2024003",
                "major": EuljiMajor.MEDICAL_IT,
                "grade": 2,
                "email": "medicalit01@eulji.ac.kr",
                "phone": "010-3456-7890",
                "address": "대전광역시 중구 을지로"
            },
            {
                "name": "정을지",
                "student_number": "2024004",
                "major": EuljiMajor.NURSING,
                "grade": 1,
                "email": "nursing02@eulji.ac.kr",
                "phone": "010-4567-8901",
                "address": "대전광역시 중구 을지로"
            },
            {
                "name": "최GPT",
                "student_number": "2024005",
                "major": EuljiMajor.MEDICAL_IT,
                "grade": 4,
                "email": "medicalit02@eulji.ac.kr",
                "phone": "010-5678-9012",
                "address": "대전광역시 중구 을지로"
            }
        ]
        
        # 학생 데이터 삽입
        created_students = []
        for student_data in students_data:
            student = EuljiStudent(**student_data)
            db.add(student)
            created_students.append(student)
        
        db.commit()
        print(f"✅ {len(created_students)}명의 을지대학교 학생 데이터가 생성되었습니다.")
        
        # 을지대학교 을GPT 프로젝트 샘플 데이터
        projects_data = [
            {
                "title": "을지대학교 AI 진단 지원 시스템",
                "description": "의료 영상을 분석하여 질병 진단을 지원하는 AI 시스템 개발",
                "category": "AI프로젝트",
                "status": ProjectStatus.IN_PROGRESS,
                "team_leader_id": created_students[1].id  # 박방사 (방사선학과 4학년)
            },
            {
                "title": "을지대학교 환자 관리 웹 플랫폼",
                "description": "병원 내 환자 정보 관리 및 예약 시스템 웹 개발",
                "category": "웹개발",
                "status": ProjectStatus.PLANNING,
                "team_leader_id": created_students[4].id  # 최GPT (의료IT학과 4학년)
            },
            {
                "title": "을지대학교 간호 교육 모바일 앱",
                "description": "간호학과 학생들을 위한 실습 가이드 및 학습 모바일 애플리케이션",
                "category": "모바일앱",
                "status": ProjectStatus.COMPLETED,
                "team_leader_id": created_students[0].id  # 김간호 (간호학과 3학년)
            },
            {
                "title": "을지대학교 의료기기 IoT 모니터링",
                "description": "의료기기 상태 모니터링 및 예방정비 IoT 시스템",
                "category": "의료시스템",
                "status": ProjectStatus.IN_PROGRESS,
                "team_leader_id": created_students[2].id  # 이의료 (의료IT학과 2학년)
            }
        ]
        
        # 프로젝트 데이터 삽입
        created_projects = []
        for project_data in projects_data:
            project = EuljiProject(**project_data)
            db.add(project)
            created_projects.append(project)
        
        db.commit()
        print(f"✅ {len(created_projects)}개의 을지대학교 을GPT 프로젝트가 생성되었습니다.")
        
        # 프로젝트 멤버 관계 설정
        project_members = [
            # AI 진단 지원 시스템 팀
            ProjectMember(project_id=created_projects[0].id, student_id=created_students[1].id, role="팀장"),
            ProjectMember(project_id=created_projects[0].id, student_id=created_students[4].id, role="개발자"),
            
            # 환자 관리 웹 플랫폼 팀
            ProjectMember(project_id=created_projects[1].id, student_id=created_students[4].id, role="팀장"),
            ProjectMember(project_id=created_projects[1].id, student_id=created_students[2].id, role="개발자"),
            
            # 간호 교육 모바일 앱 팀
            ProjectMember(project_id=created_projects[2].id, student_id=created_students[0].id, role="팀장"),
            ProjectMember(project_id=created_projects[2].id, student_id=created_students[3].id, role="기획자"),
            
            # IoT 모니터링 시스템 팀
            ProjectMember(project_id=created_projects[3].id, student_id=created_students[2].id, role="팀장"),
            ProjectMember(project_id=created_projects[3].id, student_id=created_students[1].id, role="기술자문"),
        ]
        
        for member in project_members:
            db.add(member)
        
        db.commit()
        print(f"✅ {len(project_members)}개의 프로젝트 멤버 관계가 생성되었습니다.")
        
        print("\n" + "=" * 60)
        print("🎉 을지대학교 을GPT MariaDB 초기 설정이 완료되었습니다!")
        print("=" * 60)
        print("📊 생성된 데이터:")
        print(f"  • 학생: {len(created_students)}명")
        print(f"  • 프로젝트: {len(created_projects)}개")
        print(f"  • 프로젝트 멤버: {len(project_members)}개 관계")
        print("\n🚀 이제 FastAPI 서버를 실행할 수 있습니다:")
        print("  uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 샘플 데이터 생성 중 오류: {str(e)}")
        raise
    finally:
        db.close()

def main():
    """메인 함수"""
    print("=" * 60)
    print("🏥 을지대학교 을GPT MariaDB 초기 설정")
    print("=" * 60)
    
    # MariaDB 연결 테스트
    print("1. MariaDB 연결 테스트...")
    if not test_mariadb_connection():
        print("❌ MariaDB 연결에 실패했습니다. 설정을 확인해주세요.")
        return False
    
    # 테이블 생성
    print("\n2. 테이블 생성...")
    create_tables()
    
    # 샘플 데이터 삽입
    print("\n3. 샘플 데이터 삽입...")
    insert_sample_data()
    
    return True

if __name__ == "__main__":
    main()
