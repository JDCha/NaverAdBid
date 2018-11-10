from selenium import webdriver
from openpyxl import load_workbook
from bs4 import BeautifulSoup

import time

browser = webdriver.Chrome("/Users/itaegyeong/PycharmProjects/NaverAd/data/chromedriver")


def load_data_file():
    wb = load_workbook('/Users/itaegyeong/PycharmProjects/NaverAd/data/data.xlsx')
    sheet1 = wb['Sheet']

    data_list = list(sheet1.rows)
    dict_data_list = list()

    for index, item in enumerate(data_list):
        if index == 0:
            continue

        data_dict = {}
        data_dict['group_id'] = item[0].value
        data_dict['group_name'] = item[1].value
        data_dict['status'] = item[2].value
        data_dict['keyword_count'] = item[3].value
        data_dict['pc_url'] = item[4].value
        data_dict['mobile_url'] = item[5].value
        data_dict['keyword_id'] = item[6].value
        data_dict['keyword_name'] = item[7].value
        data_dict['current_bid'] = item[8].value
        data_dict['hope_rank'] = item[9].value
        data_dict['plus_minus_money'] = item[10].value
        data_dict['current_rank'] = item[11].value
        data_dict['pc_ad_count'] = item[12].value
        data_dict['mobile_ad_count'] = item[12].value
        data_dict['domain'] = item[13].value

        dict_data_list.append(data_dict)

    return dict_data_list


def return_html(browser_page_source):
    html = BeautifulSoup(browser_page_source, "html.parser")
    return html


def naver_login(id, pw, dict_data_list):
    browser.get("https://searchad.naver.com")

    browser.find_element_by_xpath('//*[@id="uid"]').send_keys(id)
    browser.find_element_by_xpath('//*[@id="upw"]').send_keys(pw)
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="container"]/main/div/div[1]/home-login/div/fieldset/span/button').click()
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="container"]/my-screen/div/div[1]/div/my-screen-board/div/div[1]/ul/li[1]/a').click()
    time.sleep(5)

    for item in dict_data_list:
        keyword_id = item['keyword_id']

        browser.switch_to.window(browser.window_handles[1])
        time.sleep(3)

        browser.find_element_by_xpath(
            '//*[@id="wrap"]/div/div/div[1]/div[2]/div/div[2]/div/div/div/form/div/input').send_keys(keyword_id)

        time.sleep(3)

        browser.find_element_by_xpath('//*[@id="wrap"]/div/div/div[1]/div[2]/div/div[2]/div/div/div/form/ul/div/div/div/div/ul/li/a').click()

        time.sleep(10)
        browser.implicitly_wait(1000)

        # 노출 현황보기 클릭
        browser.execute_script("document.querySelector('#wgt-{keyword} > td:nth-child(10) > a').click();".format(keyword=keyword_id))
        browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[2]/div[2]/div[3]')

        html = return_html(browser.page_source)
        rank_html = html.find('div',{"class":"scroll-wrap"})

        pc_rank_list = rank_html.find_all("div",{"class":"content ng-scope"})
        item['pc_ad_count'] = len(pc_rank_list)

        # 현재 광고 순위 체크
        for i, pc_rank in enumerate(pc_rank_list):
            if item['pc_url'] == pc_rank.find('a',{'class':'lnk_tit ng-binding ng-scope'})['href']:
                item['current_rank'] = i

        time.sleep(5)

        # 모바일 칸으로 이동 및 모바일 광고 개수 크롤링
        browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[2]/div[1]/ul/li[2]/a').click()
        html = return_html(browser.page_source)
        mobile_rank_html = html.find('div', {"class": "scroll-wrap"})
        item['mobile_ad_count'] = len(mobile_rank_html.find_all("div", {"class": "content ng-scope"}))

        # 닫기 버튼 눌리기
        browser.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/div[1]/div[1]/button/i').click()

        # 순위체크
        new_bid = item['current_bid']
        if item['current_rank'] < item['hope_rank']:
            new_bid = new_bid - item['plus_minus_money']
        elif item['current_rank'] > item['hope_rank']:
            new_bid = new_bid + item['plus_minus_money']

        # 입찰 금액 변경
        browser.execute_script(
            "document.querySelector('#wgt-{keyword} > td.cell-bid-amt.text-right.txt-r > a').click();".format(keyword=keyword_id))

        bid_input_box = browser.find_element_by_xpath('//*[@id="wgt-{keyword}"]/td[5]/a/div/div/div[2]/div[1]/div/span/input'.format(keyword=keyword_id)).clear()
        bid_input_box.send_keys(new_bid)
        item['current_rank'] = new_bid

        print(item)

        break


if __name__ == '__main__':
    id = 'tourtopping'
    pw = 'xndjxhvld11'
    data = load_data_file()
    naver_login(id, pw, data)



