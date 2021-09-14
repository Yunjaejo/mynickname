import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.hh99_nickname # db연결

# db = client.nickname

# import sys
#
# sys.stdout = open('words_2.txt', 'w',encoding='UTF-8')



def wiki_words_crawler(page) :      # https://ko.wiktionary.org 를 제외한 부분을 받는다.
    url = f'https://ko.wiktionary.org{page}'   # 현재 페이지
    for re in range(150):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(f'{url}', headers=headers)

        #
        # page = 'https://ko.wiktionary.org/w/index.php?title=%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%EB%AA%85%EC%82%AC'
        soup = BeautifulSoup(data.text, 'html.parser')

        trs = soup.select('#mw-pages')
        for tr in trs:
            rink = tr.select_one('a:nth-child(4)')['href']     # 다음페이지 링크
            word = soup.select('#mw-pages > div > div > div > ul > li')     # 낱말 경로
            url = f'https://ko.wiktionary.org{rink}'    # 다음페이지 링크를 url로 넘겨준다.
            for b in word:
                words = b.select_one('a').text   # 낱말 추출
                if len(words) > 1 :  # 1글자 이상만 구함
                    # print(words)

                    doc = {
                        'word':words,
                        'class':'noun'             # 명사
                    }
                    db.wordsdb.insert_one(doc)


#mw-pages > div > div > div:nth-child(1) > ul > li:nth-child(1) > a

#mw-pages > div > div > div:nth-child(12) > ul > li:nth-child(7) > a    # nth-child는 지워도 된다
#mw-pages > div > div
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://ko.wiktionary.org/wiki/%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%EA%B4%80%ED%98%95%EC%82%AC%ED%98%95(%ED%98%95%EC%9A%A9%EC%82%AC)', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser') # c의 주소를 받아온다
trs = soup.select('#mw-pages > div > div > div > ul > li') # 형용사 크롤링
for tr in trs :
    words = tr.select_one('a').text
    doc = {
        'word': words,
        'class': 'adj'  # 형용사
    }
    db.wordsdb.insert_one(doc)

    print(words)




wiki_words_crawler('/w/index.php?title=%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%EB%AA%85%EC%82%AC&from=%EA%B0%80')   # 명사 크롤링
