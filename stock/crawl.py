import requests
from bs4 import BeautifulSoup

# #네이버 주식 시가총액 목록 가져오기
# url = "https://finance.naver.com/sise/sise_market_sum.nhn?page=1"
# res = requests.get(url)
# soup = BeautifulSoup(res.text,'lxml')

# stock_head  = soup.find("thead").find_all("th")
# data_head = [head.get_text() for head in stock_head]

# # print(data_head)

# stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")

# for stock in stock_list:
#   if len(stock) > 1:
#     print(stock.get_text().split())

url = "https://finance.naver.com/sise/sise_market_sum.nhn"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

stockTop50_corp = soup.find("table",attrs={"class":"type_2"}).find("tbody").find_all("a",  attrs={"class":"tltle"})
def getDataOfParam(param):
  
    sub_tbody = sub_soup.find("table", attrs={"class": "tb_type1 tb_num tb_type1_ifrs"}).find("tbody")
    sub_title = sub_tbody.find("th", attrs={"class": param}).get_text().strip()

    # param에 매핑되는 row 검색 => 상위 이동 => 해당 row의 모든 td 컬럼 가져오기
    dataOfParam = sub_tbody.find("th", attrs={"class": param}).parent.find_all("td")
    value_param = [i.get_text().strip() for i in dataOfParam]

    print(sub_title, " : ", value_param)
    return value_param

ParamList = ['매출액','영업이익','당기순이익','ROE(지배주주)','PER(배)','PBR(배)']

for idx, pText in enumerate(ParamList):
  param = "".join(subsoup.find('strong',text=pText).parent['class'])
  getDataOfParam(param)


