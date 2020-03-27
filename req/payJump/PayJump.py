#!/usr/bin/python
# -*- coding: UTF-8 -*-
# from urllib3 import encode_multipart_formdata
import requests, random, string, json, time, os
from requests_toolbelt.multipart.encoder import MultipartEncoder
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

GATEWAY_HOST = 'resapi.wondershare.com'
COOKIE_PATH = os.getcwd() + "//cookies.json"
USERNAME = "82830943@163.com"
PASS = "123456"


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver

def save_cookies(driver, filepath=COOKIE_PATH):
    cookie = driver.get_cookies()
    # c = json.dumps(cookie,indent=4)
    # print(c)
    jsonCookies = json.dumps(cookie)
    # 登录完成后，将cookie保存到本地文件
    with open(filepath, 'w') as f:
        f.write(jsonCookies)


def use_cookies(driver, filepath=COOKIE_PATH):
    # 删除第一次建立连接时的cookie
    driver.delete_all_cookies()
    # 读取登录时存储到本地的cookie
    with open(filepath, 'r') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        driver.add_cookie({
            'domain': cookie['domain'],
            'secure': cookie['secure'],
            'value': cookie['value'],
            'path': cookie['path'],
            'expires': cookie['value'],
            'httpOnly': cookie['httpOnly'],
            'name': cookie['name']
        })


def v_productName(driver, name):
    assert name in driver.find_element_by_css_selector("span.tit>a").text, "productName is not Equal"


def login(driver):
    driver.find_element_by_name("mail").send_keys(USERNAME)
    driver.find_element_by_name("pass").send_keys(PASS)
    driver.find_element_by_css_selector("form[data-form='login']>div>button").click()


def v_cookie(driver,filepath=COOKIE_PATH):
    if os.path.exists(filepath):
        if os.path.getsize(filepath):
            print("cookie is wxist")
            return True
        else:
            return False
    else:
        return False



def get_now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


if __name__ == "__main__":
    pass
    print get_now()
    url = "https://effects.wondershare.com/#popLogin"
    driver = get_driver()
    driver.get(url)
    driver.implicitly_wait(60)
    driver.save_screenshot("1.png")
    # if v_cookie(driver):
    #     use_cookies(driver)
    # else:
    #     login(driver)
    #     save_cookies(driver)
    # url = "https://effects.wondershare.com/go-pay.html?buy_url=HNbrB6YR-BksF17Nxq7Q9Mp5m14uUZlNV3HnNB6Ag0-sseGLP30Rdi3eOVQu5RF0u8uG_78ADO4sBQJRw13NTNL5PNwuEr_5hTgWEh6H7TQ2PEtJqdn4xED0AKCzz8GsAaINxR1dd4ea5RTh15acmuzCrzqynkWrQFmPD89kkX3FPccVKICfVlXi2QYdgvHIcX7-1YqzSDitRt16S8WPun1DD915Xi_nRLmkRWOaoa4lO5CT_d-PrWksN2CKTMJ8"
    # driver.get(url)
    # print driver.find_element_by_css_selector("span.tit>a").text
    # print driver.find_element_by_css_selector("td.ac>span").text
    # driver.quit()
    # print get_now()
