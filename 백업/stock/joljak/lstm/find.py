import pandas as pd

# 데이터 불러오기
workbook = pd.read_excel('stock_data.xlsx')

# 단축코드 컬럼에서 숫자가 아닌 부분을 찾기
invalid_codes = []
for code in workbook['단축코드']:
    try:
        int(code)
    except ValueError:
        invalid_codes.append(code)

# 숫자가 아닌 부분 출력
print("숫자가 아닌 부분:", invalid_codes)
