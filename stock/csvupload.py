import os
import pandas as pd
from sqlalchemy import create_engine

# MySQL 연결 정보 설정
user = 'root'
password = '1324'
host = '127.0.0.1'
database = 'kospistocks'
port = '3306'

# MySQL 연결 엔진 생성
engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}:{port}/{database}')

# CSV 파일이 있는 폴더 경로 설정
folder_path = r'C:\Apache24\flask\app\stock\data\A_lstm'

# 폴더 내의 모든 파일을 탐색
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)

        # CSV 파일 읽기
        df = pd.read_csv(file_path)

        # 데이터베이스에 데이터 쓰기
        table_name = file.replace('.csv', '')  # 파일 이름에서 확장자 제거
        df.to_sql(name=table_name, con=engine, index=False, if_exists='replace')

        print(f'{file}이(가) MySQL에 성공적으로 업로드되었습니다.')
