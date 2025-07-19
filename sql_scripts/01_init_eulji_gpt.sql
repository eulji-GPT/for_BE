-- 을지대학교 을GPT MariaDB 초기 설정 스크립트
-- 데이터베이스 및 사용자 설정

-- 한글 지원을 위한 문자셋 설정 확인
SHOW VARIABLES LIKE 'character_set%';
SHOW VARIABLES LIKE 'collation%';

-- 을지대학교 을GPT 데이터베이스 문자셋 설정
ALTER DATABASE eulji_gpt_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 시간대 설정 (한국 시간)
SET time_zone = '+09:00';

-- 을지대학교 을GPT 전용 사용자 추가 권한 설정
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON eulji_gpt_db.* TO 'eulji_user'@'%';
FLUSH PRIVILEGES;

-- 데이터베이스 상태 확인
SELECT 
    SCHEMA_NAME as '데이터베이스',
    DEFAULT_CHARACTER_SET_NAME as '문자셋',
    DEFAULT_COLLATION_NAME as '콜레이션'
FROM INFORMATION_SCHEMA.SCHEMATA 
WHERE SCHEMA_NAME = 'eulji_gpt_db';

-- 사용자 권한 확인
SHOW GRANTS FOR 'eulji_user'@'%';

-- 을지대학교 을GPT 프로젝트 초기 설정 완료 메시지
SELECT '을지대학교 을GPT MariaDB 초기 설정이 완료되었습니다!' as 메시지;
