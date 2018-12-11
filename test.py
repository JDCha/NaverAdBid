from selenium import webdriver
from bs4 import BeautifulSoup
import time

#해당 트위터 링크, 사진이 있다면 사진, 트위터안의 링크, 리트윗은 배제

# 12 -> 트위터링크, 사진, 텍스트, 리트윗 배제
# 13 -> 프로그램화(DB에다가 데이터를 저장) + selenium, request(트위터크롤링 도전), 프록시를 설정
# 14 -> Slack 으로 전송(Atoms 참고해서 Slack에 데이터를 전송)
# 15 -> 전체 마무리
# 16 -> 추가적으로 넣고싶은 기능, 메모리오류(24, 프로그램을 재실행)

keywords=['New Balance','bag']

browser=webdriver.Chrome('/Users/itaegyeong/PycharmProjects/NaverAd/data/chromedriver')
site_list=open('site_list.txt', 'r')


for site in site_list.readlines():

    browser.get(site)
    html=BeautifulSoup(browser.page_source, 'html.parser')

    tweets = html.find_all('li',{'class':'js-stream-item stream-item stream-item '})

    for tw in tweets:
        tw_text = tw.find('p',{'class':'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'}).text
        tw_medias = tw.find_all('div',{'class':'AdaptiveMedia-container'})

        tw_link = 'https://twitter.com/{id}/status/{tw_id}'.format(id=site.split('/')[-1], tw_id=tw['data-item-id'])
        print(tw_link)

        tw_retweet = tw.find('span',{'class':'js-retweet-text'})

        if tw_retweet is None:
            for tw_m in tw_medias:
                imgs = tw_m.find_all('img')
                for img in imgs:
                    print(img['src'])

            print()

