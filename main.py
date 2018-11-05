from selenium import webdriver
from openpyxl import load_workbook
import time

browser = webdriver.Chrome("/data/chromedriver")


def load_data_file():
    wb = load_workbook('data.xlsx')
    sheet1 = wb['Sheet']

    print(sheet1.cell(row=1, column=1).value)

    print(sheet1.rows)



def naver_login(id, pw):
    browser.get("https://searchad.naver.com")
    browser.find_element_by_xpath('//*[@id="uid"]').send_keys(id)
    browser.find_element_by_xpath('//*[@id="upw"]').send_keys(pw)
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="container"]/my-screen/div/div[1]/div/my-screen-board/div/div[1]/ul/li[1]/a').click()


if __name__ == '__main__':
    id = input("id를 입력해주세요 : ")
    pw = input("pw를 입력해주세요 : ")

