from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas

browser = webdriver.Chrome("/Users/itaegyeong/PycharmProjects/NaverAd/data/chromedriver")


def load_data_file():
    df = pandas.read_excel('/Users/itaegyeong/PycharmProjects/NaverAd/data/test_data.xlsx')
    df = df.to_dict('records')
    return df


def return_html(browser_page_source):
    html = BeautifulSoup(browser_page_source, "html.parser")
    return html


def process(id, pw, dict_data_list):

    # 홈페이지 접속 및 로그인, 광고시스템 클릭
    browser.get("https://searchad.naver.com")
    browser.find_element_by_xpath('//*[@id="uid"]').send_keys(id)
    browser.find_element_by_xpath('//*[@id="upw"]').send_keys(pw)
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="container"]/main/div/div[1]/home-login/div/fieldset/span/button').click()
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="container"]/my-screen/div/div[1]/div/my-screen-board/div/div[1]/ul/li[1]/a').click()
    time.sleep(5)

    # 키워드 금액별로 반복문 사용
    for item in dict_data_list:
        keyword_id = item['keyword_id']

        browser.switch_to.window(browser.window_handles[1])
        time.sleep(3)

        # 키워드 검색
        browser.find_element_by_xpath(
            '//*[@id="wrap"]/div/div/div[1]/div[2]/div/div[2]/div/div/div/form/div/input').send_keys(keyword_id)

        time.sleep(3)

        browser.find_element_by_xpath('//*[@id="wrap"]/div/div/div[1]/div[2]/div/div[2]/div/div/div/form/ul/div/div/div/div/ul/li/a').click()

        time.sleep(5)
        browser.implicitly_wait(1000)

        # 노출 현황보기 클릭
        browser.execute_script("document.querySelector('#wgt-{keyword} > td:nth-child(10) > a').click();".format(keyword=keyword_id))
        browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[2]/div[2]/div[3]')

        html = return_html(browser.page_source)
        rank_html = html.find('div',{"class":"scroll-wrap"})

        # PC 광고 개수 크롤링
        pc_rank_list = rank_html.find_all("div",{"class":"content ng-scope"})
        item['pc_ad_count'] = len(pc_rank_list)

        # 현재 광고 순위 체크
        for i, pc_rank in enumerate(pc_rank_list):
            if item['domain'] == pc_rank.find('a',{'class':'lnk_tit ng-binding ng-scope'})['href']:
                item['current_rank'] = i

        time.sleep(5)

        # 모바일 칸으로 이동 및 모바일 광고 개수 크롤링
        browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[2]/div[1]/ul/li[2]/a').click()
        html = return_html(browser.page_source)
        mobile_rank_html = html.find('div', {"class": "scroll-wrap"})
        item['mobile_ad_count'] = len(mobile_rank_html.find_all("div", {"class": "content ng-scope"}))

        # 닫기 버튼 눌리기
        browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[1]/div[1]/button/i').click()

        # 입찰 금액 변경 클릭
        browser.execute_script(
            "document.querySelector('#wgt-{keyword} > td.cell-bid-amt.text-right.txt-r > a').click();".format(keyword=keyword_id))

        bid_input_box = browser.find_element_by_xpath('//*[@id="wgt-{keyword}"]/td[5]/a/div/div/div[2]/div[1]/div/span/input'.format(keyword=keyword_id))

        # 현재 입찰 금액 받아오기
        item['current_bid'] = int(bid_input_box.get_attribute('value'))

        # 순위체크
        new_bid = item['current_bid']

        if item['current_rank'] < item['hope_rank']:
            new_bid = new_bid - item['plus_minus_money']
        elif item['current_rank'] > item['hope_rank']:
            new_bid = new_bid + item['plus_minus_money']

        # 순위 같으면 변경 안함
        if item['current_rank'] == item['hope_rank']:
            item['check'] = 'rank success'
            continue

        # 입찰금액보다 오버 됫을 경우 변경 안하고 check항목을 fail로 변경
        if new_bid > item['max_bid']:
            item['check'] = 'max bid over'
            continue
        elif new_bid < 70:
            item['check'] = '70 이하로 내려갈 수 없습니다'
            new_bid = 70
        else:
            item['check'] = 'bid changing'


        bid_input_box.clear()
        bid_input_box.send_keys(new_bid)

        # 변경 버튼 클릭
        browser.execute_script(
            "document.querySelector('#wgt-{keyword} > td.cell-bid-amt.text-right.txt-r > a > div > div > div.popover-content > div.form-inline > div > button.btn.btn-primary.editable-submit').click();".format(keyword=keyword_id))

        time.sleep(2)

        # 변경 알림사항 닫기 버튼
        browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[3]/button').click()
        item['current_bid'] = new_bid

        time.sleep(1)

    df = pandas.DataFrame(dict_data_list)  # pandas 사용 l의 데이터프레임화
    df.to_excel('/Users/itaegyeong/PycharmProjects/NaverAd/data/test_data.xlsx', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
    id = 'tourtopping'
    pw = 'xndjxhvld11'
    data = load_data_file()
    process(id, pw, data)

