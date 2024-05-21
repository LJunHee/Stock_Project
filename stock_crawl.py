import datetime as dt
import requests
from bs4 import BeautifulSoup

# 날짜 형식을 변환하는 함수
def date_format(d):
    d = str(d).replace('-', '.')
    yyyy, mm, dd = map(int, d.split('.'))
    return dt.date(yyyy, mm, dd)

# 네이버 금융에서 주가 지수를 가져오는 함수
def historical_index_naver(index_cd, max_pages=10):
    historical_prices = []
    page_n = 1
    last_page = None

    while page_n <= max_pages:
        try:
            naver_index = f'https://finance.naver.com/sise/sise_index_day.nhn?code={index_cd}&page={page_n}'
            response = requests.get(naver_index)
            source = BeautifulSoup(response.content, 'lxml')

            date_elements = source.find_all('td', 'date')
            price_elements = source.find_all('td', 'number_1')

            # 날짜와 닫힘 가격을 추출하여 리스트에 추가
            for n in range(len(date_elements)):
                date_text = date_elements[n].text.strip()
                if date_text.split('.')[0].isdigit():
                    this_date = date_format(date_text)
                    this_close = float(price_elements[n * 4].text.replace(',', ''))
                    historical_prices.append([this_date, this_close])

            # 마지막 페이지 번호를 한 번만 추출
            if last_page is None:
                last_page_element = source.find('td', 'pgRR')
                if last_page_element:
                    last_page_href = last_page_element.find('a')['href']
                    last_page = int(last_page_href.split('=')[-1])
                else:
                    last_page = page_n

            # 페이지 증가
            page_n += 1

            # 종료 조건 확인
            if page_n > last_page:
                break

        except Exception as e:
            print(f"Error on page {page_n}: {e}")
            break

    return historical_prices

# 함수 호출 예시
historical_prices = historical_index_naver('KPI100')
print(historical_prices)
