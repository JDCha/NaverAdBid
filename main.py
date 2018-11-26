
# "시간설정을 했으면좋겠다." = 09:00~18:00/////// 18시00부터 다음날 새벽4시나 다음날아침 9:00 시의설정이 불가한듯하다
#
# 0 오류가 뜬다  =  0오류(페이지가 에러가나서)가 뜨면 순위가 없는걸로인식 입찰가를 올린다(입찰가를 올리면안되요)
#
# 0 오류를 안뜨게하는 방법은 없을까...0이뜨면 새로고침?
#
# 몇시간 테스트결과 마무리 확인창이 안눌러져서 멈춰있는경우를 2~3번 보았다.. 이 경우가 없었으면좋겠다
#
# 5시간정도 돌아갔는데 3백? 4백 몇백개째에서 메모리부족현상 (현재 8기가) 프로그램이 돌아가지 않았다..(메모리부족화면노출)

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.


class NaverAdSystem:

    def __init__(self, webdriver_path, data_file_path, id, pw):
        self.browser = webdriver.Chrome(webdriver_path)

        self.df = pandas.read_excel(data_file_path)
        self.df = self.df.to_dict('records')

        self.id = id
        self.pw = pw

    # html 코드를 Beautifulsoup을 이용해 파싱한 결과로 반환하는 함수
    def return_html(self, browser_page_source):
        html = BeautifulSoup(browser_page_source, "html.parser")
        return html

    # 딜레이 함수
    def wait(self, code, division, delay_second):
        if division == "xpath":
            my_division = By.XPATH
        elif division == "css":
            my_division = By.CSS_SELECTOR
        else:
            my_division = By.CLASS_NAME

        try:
            element = WebDriverWait(self.browser, delay_second).until(EC.presence_of_element_located((my_division, code)))
        except:
            return -1

    # 홈페이지 접속 및 로그인, 광고시스템 클릭
    def naver_login(self, id, pw):

        # 홈페이지 접속 및, 로그인화면이 뜰때까지 wait
        self.browser.get("https://searchad.naver.com")
        self.wait('//*[@id="uid"]', "xpath", 10)

        # 아이디와 비밀번호 입력 후 로그인, 광고 시스템창이 뜰때까지 wait
        self.browser.find_element_by_xpath('//*[@id="uid"]').send_keys(id)
        self.browser.find_element_by_xpath('//*[@id="upw"]').send_keys(pw)
        self.browser.find_element_by_xpath(
            '//*[@id="container"]/main/div/div[1]/home-login/div/fieldset/span/button').click()
        self.wait('//*[@id="container"]/my-screen/div/div[1]/div/my-screen-board/div/div[1]/ul/li[1]/a', "xpath", 10)

        # 광고 시스템창 클릭 후 혹시모를 에러를 대비해 1초 wait
        self.browser.find_element_by_xpath(
            '//*[@id="container"]/my-screen/div/div[1]/div/my-screen-board/div/div[1]/ul/li[1]/a').click()
        self.browser.implicitly_wait(1000)

        # 광고 시스템창으로 탭 이동
        self.browser.switch_to.window(self.browser.window_handles[1])

    # 키워드 검색, 노출현황보기 클릭 후 html 코드 반환
    def search_keyword(self, keyword_id):
        # 키워드를 검색하고, 노출현황보기창이 뜰떄까지 wait
        self.browser.find_element_by_xpath(
            '//*[@id="wrap"]/div/div/div[1]/div[2]/div/div[2]/div/div/div/form/div/input').send_keys(keyword_id)
        self.wait('//*[@id="wrap"]/div/div/div[1]/div[2]/div/div[2]/div/div/div/form/ul/div/div/div/div/ul/li/a',
             "xpath", 10)
        self.browser.find_element_by_xpath(
            '//*[@id="wrap"]/div/div/div[1]/div[2]/div/div[2]/div/div/div/form/ul/div/div/div/div/ul/li/a').click()
        self.wait('#wgt-{keyword} > td:nth-child(10) > a'.format(keyword=keyword_id), "css", 10)

        # 노출 현황보기 클릭
        self.browser.execute_script(
            "document.querySelector('#wgt-{keyword} > td:nth-child(10) > a').click();".format(keyword=keyword_id))
        self.browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[2]/div[2]/div[3]')

        # 노출현황보기창의 코드를 반환
        html = self.return_html(self.browser.page_source)
        return html

    # pc 순위 체크 및, 현재 순위 반영
    def pc_rank(self, html, item):
        rank_html = html.find('div', {"class": "scroll-wrap"})

        # PC 광고 개수 크롤링
        pc_rank_list = rank_html.find_all("div", {"class": "content ng-scope"})
        item['pc_ad_count'] = len(pc_rank_list)

        # 현재 pc 광고 순위 체크
        flag = False
        for i, pc_rank in enumerate(pc_rank_list):
            if item['pc_url'] == pc_rank.find('a', {'class': 'lnk_url ng-binding'}).text:
                item['pc_current_rank'] = i + 1
                flag = True

        if flag is False:
            item['pc_current_rank'] = -1

        self.browser.implicitly_wait(300)

    # mobile 순위 체크 및, 현재 순위 반영
    def mobile_rank(self, item):

        self.browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[2]/div[1]/ul/li[2]/a').click()
        html = self.return_html(self.browser.page_source)

        mobile_rank_html = html.find('div', {"class": "scroll-wrap"})
        mobile_rank_list = mobile_rank_html.find_all("div", {"class": "content ng-scope"})

        # mobile 광고 개수 크롤링
        item['mobile_ad_count'] = len(mobile_rank_list)

        # 현재 mobile 광고 순위 체크
        flag = False
        for i, mobile_rank in enumerate(mobile_rank_list):
            if item['mobile_url'] == mobile_rank.find('cite', {'class': 'url'}).find('a', {'class': 'ng-binding'}).text:
                item['mobile_current_rank'] = i + 1
                flag = True

        if flag is False:
            item['mobile_current_rank'] = -1

        self.wait('//*[@id="wrap"]/div[1]/div/div/div/div[3]/button',"xpath",10)

        # 닫기버튼 클릭
        self.browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[3]/button').click()


    def bid_change(self, item):
        keyword_id = item['keyword_id']

        # 입찰금액 변경
        self.browser.execute_script(
            "document.querySelector('#wgt-{keyword} > td.cell-bid-amt.text-right.txt-r > a').click();".format(
                keyword=keyword_id))

        bid_input_box = self.browser.find_element_by_xpath(
            '//*[@id="wgt-{keyword}"]/td[5]/a/div/div/div[2]/div[1]/div/span/input'.format(keyword=keyword_id))

        # 현재 입찰 금액 받아오기
        item['current_bid'] = int(bid_input_box.get_attribute('value'))

        # 순위체크 후 새로운 금액 반영
        new_bid = item['current_bid']
        if item['pc_current_rank'] < item['hope_rank'] and item['pc_current_rank'] != -1:  # 순위가 높다면
            new_bid = new_bid - item['minus_money']
        elif item['pc_current_rank'] > item['hope_rank'] or item['pc_current_rank'] == -1:
            new_bid = new_bid + item['plus_money']

        # 순위 같으면 변경 안함
        if item['pc_current_rank'] == item['hope_rank']:
            item['check'] = 'rank success'
            return "same"

        # 입찰금액보다 오버 됫을 경우 변경 안하고 check 항목을 fail로 변경
        if new_bid > item['max_bid']:
            item['check'] = 'max bid over'
            new_bid = item['max_bid']
        elif new_bid < 70:
            item['check'] = '70 이하로 내려갈 수 없습니다'
            new_bid = 70
        else:
            item['check'] = 'bid changing'

        bid_input_box.clear()
        bid_input_box.send_keys(new_bid)

        # 최종 변경 버튼 클릭
        self.browser.execute_script(
            "document.querySelector('#wgt-{keyword} > td.cell-bid-amt.text-right.txt-r > a > div > div > div.popover-content > div.form-inline > div > button.btn.btn-primary.editable-submit').click();".format(
                keyword=keyword_id))

        self.wait('//*[@id="wrap"]/div[1]/div/div/div/div[3]/button', 'xpath', 10)

        # 변경 알림사항 닫기
        self.browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[3]/button').click()
        item['current_bid'] = new_bid

        self.browser.implicitly_wait(500)



    def process(self):

        # 홈페이지 접속 및 로그인, 광고시스템 클릭
        self.naver_login(self.id, self.pw)

        while True:
            for item in self.df:

                keyword_id = item['keyword_id']

                html = self.search_keyword(keyword_id) # 키워드 검색
                self.pc_rank(html, item) # pc 광고 개수 및 현재 순위 파악
                self.mobile_rank(item) # mobile 광고 개수 및 현재 순위 파악
                self.bid_change(item) # 입찰 금액 변경

                df = pandas.DataFrame(self.df)  # pandas 사용 l의 데이터프레임화
                df.to_excel('/Users/itaegyeong/PycharmProjects/NaverAd/data/test_data.xlsx', encoding='utf-8-sig', index=False)



    # if __name__ == '__main__':
    #
    #     id = 'tourtopping'
    #     pw = 'xndjxhvld11'
    #
    #     start_time = "10:00"
    #     duration = "5" # 5시간 지속 hour 단위
    #
    #     while True:
    #         now_hour = int(datetime.datetime.now().hour) # 14
    #         now_minute = int(datetime.datetime.now().minute) # 01
    #
    #         if now_hour >= int(start_time.split(":")[0]) and now_minute >= int(start_time.split(":")[1]):
    #             data = load_data_file()
    #             process(id, pw, data, start_time, duration)
    #             break
    #

naver_ad_system = NaverAdSystem('/Users/itaegyeong/PycharmProjects/NaverAd/data/chromedriver',
                                '/Users/itaegyeong/PycharmProjects/NaverAd/data/test_data.xlsx',
                                'tourtopping','xndjxhvld11')

naver_ad_system.process()
