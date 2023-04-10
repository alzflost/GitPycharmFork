import requests
from urllib.request import urlopen
import collections
from bs4 import BeautifulSoup
import ssl
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
import time
import json


def to_json(crawl_dict):
    with open('sogang_notices.json', 'w', encoding='utf-8') as file :
        json.dump(crawl_dict, file, ensure_ascii=False, indent='\t')
    return


context = ssl._create_unverified_context()

base_url = "http://www.sogang.ac.kr"
url = 'https://www.sogang.ac.kr/front/boardlist.do?bbsConfigFK=2'

list = []

response = requests.get(url, verify=False)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    title = soup.select('a')

    for i in title:
        #print(i.attrs['href'])
        if i.attrs['href'][0] == '/':
            #print(i.attrs['href'].split('¤')[0])
            if i.attrs['href'].split('?')[0] == '/Download':
                continue
            list.append([i.attrs['href'].split('¤')[0], i.text])

else:
    print(response.status_code)

crawled_notices = collections.defaultdict()

for page in list:
    time.sleep(1)
    notice_url = base_url + page[0] + '&currentPage=1&searchField=ALL&siteGubun=1&menuGubun=1&bbsConfigFK=2&searchLowItem=ALL&searchValue='
    print('currently searching ', base_url + page[0] + '&currentPage=1&searchField=ALL&siteGubun=1&menuGubun=1&bbsConfigFK=2&searchLowItem=ALL&searchValue=')
    response = requests.get(base_url + page[0] + '&currentPage=1&searchField=ALL&siteGubun=1&menuGubun=1&bbsConfigFK=2&searchLowItem=ALL&searchValue=', verify=False)
    if response.status_code != 200:
        print("NOOOOOOOOOO\n\n")
        break
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('div.subject')
    contents = soup.select('div.substance>p')
    fetched_contents = []
    # table = soup.select('div.substance>table')
    print('제목', title.get_text())
    print('내용\n')
    for i in contents:
        texts = i.get_text()
        if texts.isspace():
            continue
        fetched_contents.append(texts)
    crawled_notices[notice_url] = fetched_contents

to_json(crawled_notices)