import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.hh99_nickname # db연결

# db = client.nickname


# import sys

# sys.stdout = open('words_2.txt', 'w',encoding='UTF-8')


def wiki_words_noun_crawler(page):  # https://ko.wiktionary.org 를 제외한 부분을 받는다.
    url = f'https://ko.wiktionary.org{page}'  # 현재 페이지
    count = 0
    for re in range(150):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(f'{url}', headers=headers)

        #
        # page = 'https://ko.wiktionary.org/w/index.php?title=%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%EB%AA%85%EC%82%AC'
        soup = BeautifulSoup(data.text, 'html.parser')

        trs = soup.select('#mw-pages')
        try:
            for tr in trs:
                rink = tr.select_one('a:nth-child(4)')['href']  # 다음페이지 링크
                word = soup.select('#mw-pages > div > div > div > ul > li')  # 낱말 경로
                url = f'https://ko.wiktionary.org{rink}'  # 다음페이지 링크를 url로 넘겨준다.
                for b in word:
                    words = b.select_one('a').text  # 낱말 추출
                    if len(words) > 1:  # 1글자 이상만 구함
                        count += 1
                        # print(words)

                        doc = {
                            'word': words,
                            'class': 'noun'  # 명사
                        }
                        db.wordsdb.insert_one(doc)
        except:
            ('')
    print(str(count) + '항목 Noun DB Upload Successes!')


def wiki_words_adj_crawler():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(
        'https://ko.wiktionary.org/wiki/%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%EA%B4%80%ED%98%95%EC%82%AC%ED%98%95(%ED%98%95%EC%9A%A9%EC%82%AC)',
        headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')  # c의 주소를 받아온다
    trs = soup.select('#mw-pages > div > div > div > ul > li')  # 형용사 크롤링
    count = 0
    for tr in trs:
        count += 1
        words = tr.select_one('a').text
        doc = {
            'word': words,
            'class': 'adj'  # 형용사
        }
        db.wordsdb.insert_one(doc)
    print(str(count) + '항목 Adj DB Upload Successes!')


def wiki_animal_crawler():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(
        'https://ko.wiktionary.org/wiki/%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%ED%8F%AC%EC%9C%A0%EB%A5%98',
        headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')  # c의 주소를 받아온다
    trs = soup.select('#mw-pages > div > div > div > ul > li')  # 동물 크롤링
    count = 0
    for tr in trs:
        count += 1
        animal = tr.select_one('a').text
        doc = {
            'word': animal,
            'class': 'animal'  # 동물
        }
        db.wordsdb.insert_one(doc)

    print(str(count) + '항목 Animal DB Upload Successes!')


def wiki_fruits_crawler():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(
        'https://ko.wikipedia.org/wiki/%EB%B6%84%EB%A5%98:%EA%B3%BC%EC%9D%BC',
        headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')  # c의 주소를 받아온다
    trs = soup.select('#mw-pages > div > div > div > ul > li')  # 과일 크롤링
    count = 0
    for tr in trs:
        fruits = tr.select_one('a').text
        if len(fruits) < 5:
            if fruits != '과식주의':
                count += 1
                doc = {
                    'word': fruits,
                    'class': 'fruits'  # 과일
                }
                db.wordsdb.insert_one(doc)

    print(str(count) + '항목 Fruits DB Upload Successes!')


wiki_words_adj_crawler()  # 형용사

wiki_animal_crawler()  # 동물

wiki_fruits_crawler()  # 과일

wiki_words_noun_crawler(
    '/w/index.php?title=%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%EB%AA%85%EC%82%AC&from=%EA%B0%80')  # 명사

