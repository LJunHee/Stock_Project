import pymysql
import pandas as pd

conn = pymysql.connect(host= '127.0.0.1', user='root' , password='1324' ,charset='utf8')
workbook = pd.read_excel('KOSPI100.xlsx', index_col=0, dtype={'종목코드':str})

sql_character = '''
              CREATE TABLE KOSPI
               (ID INT NOT NULL PRIMARY KEY,
               종목명 VARCHAR(255) NULL,
               종목코드 VARCHAR(255) NULL,
               상장주식수 BIGINT NULL,
               상장일 DATE NULL,
               영문종목명 VARCHAR(255) NULL,
               주식종류 VARCHAR(7) NULL,
               증권구분 VARCHAR(15) NULL)
'''
sql_value = '''
INSERT INTO KOSPI(ID ,종목명, 종목코드, 상장주식수, 상장일, 영문종목명, 주식종류, 증권구분) VALUE(%s,%s,%s,%s,%s,%s,%s,%s)
'''
try:
  curs = conn.cursor()
  curs.execute('DROP DATABASE IF EXISTS kospistocks')
  curs.execute('CREATE DATABASE kospistocks')
  conn.select_db('kospistocks')
  curs.execute(sql_character)

  for idx,(index, row) in enumerate(workbook.iterrows(), start=1):
    if not row.isnull().any():  # 모든 열이 채워져 있는 경우에만 데이터베이스에 삽입
      data_list = [idx]  # ID 값을 추가하기 위해 첫 번째 열값으로 초기화
      data_list.append(index)
      data_list.append(row.iloc[0])

      for value in row[1:]:
        if pd.isnull(value):  # 빈 값인 경우 0으로 처리
          data_list.append(0)

        else:
          data_list.append(value)
      # print(data_list)
      curs.execute(sql_value, data_list)
    conn.commit()

    curs.execute('SELECT * FROM KOSPI')
    sql_row = curs.fetchall()
    for i in sql_row:
      print(i)

finally:
  conn.close()
