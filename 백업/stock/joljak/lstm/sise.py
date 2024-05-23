import requests
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/item/sise.naver?code=005930'

# 웹페이지 가져오기
response = requests.get(url)

if response.status_code == 200:
    # BeautifulSoup를 이용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 주요 시세 부분 추출
    main_section = soup.find('div', {'class': 'today'}).find_all('span', {'class': 'blind'})

    if main_section:
        # 주요 시세 출력
        print("현재가:", main_section[0].text)
        print("전일대비:", main_section[1].text.strip())
        print("등락률:", main_section[2].text.strip())
        print("거래량:", main_section[3].text.strip())
        print("시가총액:", main_section[4].text.strip())

        # 추가 정보 출력
        print("매도호가:", main_section[5].text.strip())
        print("매수호가:", main_section[6].text.strip())
        print("전일가:", main_section[7].text.strip())
        print("시가:", main_section[8].text.strip())
        print("고가:", main_section[9].text.strip())
        print("저가:", main_section[10].text.strip())
        print("상한가:", main_section[11].text.strip())
        print("하한가:", main_section[12].text.strip())
        print("PER:", main_section[13].text.strip())
        print("EPS:", main_section[14].text.strip())
        print("52주 최고:", main_section[15].text.strip())
        print("52주 최저:", main_section[16].text.strip())
        print("상장주식수:", main_section[17].text.strip())
        print("외국인현재:", main_section[18].text.strip())
        print("자본금:", main_section[19].text.strip())
        print("거래대금(백만):", main_section[20].text.strip())
else:
    print("웹페이지를 가져오는 데 문제가 발생했습니다. 상태 코드:", response.status_code)
