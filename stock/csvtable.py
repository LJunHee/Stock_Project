import pymysql

# MySQL 연결 정보 설정
user = 'root'
password = '1324'
host = '127.0.0.1'
database = 'kospistocks'
port = 3306

# MySQL 연결
connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)

# 커서 생성
cursor = connection.cursor()

# 테이블 이름 리스트
table_names = [
    'f&f_test_result', 'gs_test_result',
    'gs리테일_test_result', 'hd한국조선해양_test_result', 'hd현대_test_result', 'hd현대중공업_test_result', 'hmm_test_result',
    'kb금융_test_result', 'kt&g_test_result', 'kt_test_result', 'lg_test_result', 'lg디스플레이_test_result',
    'lg생활건강_test_result', 'lg에너지솔루션_test_result', 'lg유플러스_test_result', 'lg이노텍_test_result', 'lg전자_test_result',
    'lg화학_test_result', 'naver_test_result', 'nh투자증권_test_result', 'posco홀딩스_test_result', 's-oil_test_result',
    'sk 바이오팜_test_result', 'sk_test_result', 'skc_test_result', 'sk바이오사이언스_test_result', 'sk스퀘어_test_result',
    'sk아이이테크놀리지_test_result', 'sk이노베이션_test_result', 'sk텔레콤_test_result', 'sk하이닉스_test_result', '강원랜드_test_result',
    '고려아연_test_result', '금양_test_result', '금호석유_test_result', '기아_test_result', '기업은행_test_result', '넷마블_test_result',
    '대한항공_test_result', '두산밥캣_test_result', '두산에너빌리티_test_result', '롯데지주_test_result', '롯데케미칼_test_result',
    '메리츠금융지주_test_result', '미래에셋증권_test_result', '삼성sdi_test_result', '삼성sds_test_result', '삼성물산_test_result',
    '삼성바이오로직스_test_result', '삼성생명_test_result', '삼성엔지니어링_test_result', '삼성전기_test_result', '삼성전자_test_result',
    '삼성중공업_test_result', '삼성증권_test_result', '삼성카드_test_result', '삼성화재_test_result', '셀트리온_test_result',
    '신한지주_test_result', '쌍용c&e_test_result', '아모레g_test_result', '아모레퍼시픽_test_result', '에코프로머티리얼즈_test_result',
    '엔씨소프트_test_result', '오리온_test_result', '우리금융지주_test_result', '유한양행_test_result', '이마트_test_result',
    '제일기획_test_result', '카카오_test_result', '카카오뱅크_test_result', '카카오페이_test_result', '코웨이_test_result',
    '크래프톤_test_result', '포스코dx_test_result', '포스코인터내셔널_test_result', '포스코퓨처엠_test_result', '하나금융지주_test_result',
    '하이브_test_result', '한국가스공사_test_result', '한국금융지주_test_result', '한국전력_test_result', '한국타이어앤테크놀로지_test_result',
    '한국항공우주_test_result', '한미사이언스_test_result', '한미약품_test_result', '한온시스템_test_result', '한진칼_test_result',
    '한화솔루션_test_result', '한화에어로스페이스_test_result', '한화오션_test_result', '현대건설_test_result', '현대글로비스_test_result',
    '현대모비스_test_result', '현대제철_test_result', '현대차_test_result', '호텔신라_test_result'
]

# UPDATE 쿼리 실행
for table_name in table_names:
    table_name_escaped = f'`{table_name}`'  # 테이블 이름을 백틱으로 감싸줌
    sql = f"ALTER TABLE {table_name_escaped} CHANGE `Date` `날짜` VARCHAR(255);"
    cursor.execute(sql)
    connection.commit()
    print(f'{table_name} 테이블이 업데이트 되었습니다.')
    sql = f"ALTER TABLE {table_name_escaped} CHANGE `Actual Closing Price` `실제 종가` VARCHAR(255);"
    cursor.execute(sql)
    connection.commit()
    print(f'{table_name} 테이블이 업데이트 되었습니다.')
    sql = f"ALTER TABLE {table_name_escaped} CHANGE `Forecast Closing Price` `예측 종가` VARCHAR(255);"
    cursor.execute(sql)
    connection.commit()
    print(f'{table_name} 테이블이 업데이트 되었습니다.')


# 연결 닫기
connection.close()
