import requests
from bs4 import BeautifulSoup

def return_value(address):
    res = requests.get(address)
    soup = BeautifulSoup(res.content, 'html.parser')

    section = soup.find('tbody')
    items = section.find_all('tr', onmouseover="mouseOver(this)")
    for item in items:
        basic_info = item.get_text()
        sinfo = basic_info.split("\n")
        print("\t" + sinfo[1] + "\t\t" + sinfo[2] + "\t\t\t" + sinfo[3])


baseaddress = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
for i in range(1,35):
    return_value(baseaddress+str(i))
