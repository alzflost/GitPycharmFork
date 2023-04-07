import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

context = ssl._create_unverified_context()

url = 'https://www.sogang.ac.kr/front/boardlist.do?bbsConfigFK=2'

response = requests.get(url, verify=False)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    title = soup.select('a')
    #title = soup.select_one('body > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > a')
    for i in title:
        print("\n\n공지\n")
        print(i)
else:
    print(response.status_code)