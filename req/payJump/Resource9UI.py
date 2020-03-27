#!/usr/bin/python
# -*- coding: UTF-8 -*-
# from urllib3 import encode_multipart_formdata
import requests, random, string, json, time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from req.utils.mysqldbUtil import MysqldbHelper

GATEWAY_HOST = 'resapi.wondershare.com'
COOKIE_PATH = os.getcwd() + "//cookies_resource.json"
USERNAME = "82830943@163.com"
PASS = "123456"


def find_Ele(driver, *loc):
    try:
        # 确保元素是可见的。
        # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
        #            WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
        # 注意：以下入参本身是元组，不需要加*
        time.sleep(0.3)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(loc))
        return driver.find_element(*loc)
    except:
        print u"页面中未能找到%s  %s 元素" % (loc)


def find_Eles(driver, *loc):
    time.sleep(0.2)
    return driver.find_elements(*loc)


def send_key(driver, val, *loc):
    ele = find_Ele(driver, *loc)
    ele.clear()
    ele.send_keys(val)
    # ele.send_keys(unicode(val, "utf-8"))

# def send_key2(driver, val, *loc):
#     time.sleep(0.2)
#     ele = driver.find_element(*loc)
#     ele.clear()
#     ele.send_keys(val)


def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
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
    driver.find_element_by_name("account").send_keys("wondershare")
    driver.find_element_by_name("password").send_keys("wondershare")
    time.sleep(5)
    driver.find_element_by_css_selector("div>button").click()


def v_cookie(driver, filepath=COOKIE_PATH):
    if os.path.exists(filepath):
        if os.path.getsize(filepath):
            print("cookie is exist")
            return True
        else:
            return False
    else:
        return False


def get_now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def replace_space(data):
    if u" – " in data:
        data = data.split(u" – ")[1]
    print data
    symbol = (" & ", "  ", " ")
    for i in symbol:
        data = data.replace(i, "_")
    return data

# 配置pack9链接
def pack_ui(driver):
    if v_cookie(driver):
        use_cookies(driver)
    else:
        login(driver)
        save_cookies(driver)
    find_Ele(driver, By.ID, "_M497").click()
    time.sleep(0.5)
    if "block" in find_Ele(driver, By.CSS_SELECTOR, "ul.page-sidebar-menu>li:nth-child(3)>ul").get_attribute("style"):
        find_Ele(driver, By.ID, "_MP508").click()
    else:
        find_Ele(driver, By.CSS_SELECTOR, "ul.page-sidebar-menu>li:nth-child(3)>a").click()
        find_Ele(driver, By.ID, "_MP508").click()
    driver.switch_to.frame("right")
    for i in range(13, 0, -1):
        find_Ele(driver, By.XPATH, "//li/a[contains(text(),'" + str(i) + "')]").click()
        tr = find_Eles(driver, By.CSS_SELECTOR, ".table-list>table>tbody>tr")
        print len(tr)
        i = 0
        for ele in tr:
            try:
                i = i + 1
                find_Ele(driver, By.CSS_SELECTOR, "tbody>tr:nth-child(" + str(i) + ")>td>a:nth-child(2)").click()
                val = find_Ele(driver, By.ID, "title").get_attribute("value")
                print val
                find_Ele(driver, By.CSS_SELECTOR, ".packs+input").click()
                driver.switch_to.default_content()
                driver.switch_to.frame("Openadd")
                find_Ele(driver, By.CSS_SELECTOR, ".search_form>input").send_keys(replace_space(val))
                find_Ele(driver, By.CSS_SELECTOR, "#search").click()
                time.sleep(1)
                li = find_Eles(driver, By.CSS_SELECTOR, ".pack_list>ul>li")
                # print li
                if len(li) == 1:
                    find_Ele(driver, By.CSS_SELECTOR, ".pack_list>ul>li").click()
                elif len(li) > 1:
                    n = 0
                    for ele in li:
                        n = n + 1
                        element = driver.find_element_by_css_selector(
                            ".pack_list>ul>li:nth-child(" + str(n) + ")>input")
                        # element = find_Ele(driver, By.CSS_SELECTOR, ".pack_list>ul>li:nth-child(" + str(n) + ")>input")
                        print element.get_attribute("value")
                        if element.get_attribute("value") == replace_space(val):
                            ele.click()
                driver.switch_to.default_content()
                find_Ele(driver, By.CSS_SELECTOR, ".aui_state_highlight").click()
                time.sleep(1)
                driver.switch_to.frame("right")
                find_Ele(driver, By.NAME, "dosubmit").click()
                # find_Ele(driver, By.XPATH, "//li/a[contains(text(),'" + str(i) + "')]").click()
            except Exception as err:
                print(err)
                print "操作失败"


def set_ui(driver):
    if v_cookie(driver):
        use_cookies(driver)
    else:
        login(driver)
        save_cookies(driver)
    find_Ele(driver, By.ID, "_M497").click()
    time.sleep(0.5)
    if "block" in find_Ele(driver, By.CSS_SELECTOR, "ul.page-sidebar-menu>li:nth-child(3)>ul").get_attribute("style"):
        find_Ele(driver, By.ID, "_MP509").click()
    else:
        find_Ele(driver, By.CSS_SELECTOR, "ul.page-sidebar-menu>li:nth-child(3)>a").click()
        find_Ele(driver, By.ID, "_MP509").click()
    driver.switch_to.frame("right")
    for i in range(3, 0, -1):
        find_Ele(driver, By.XPATH, "//li/a[contains(text(),'" + str(i) + "')]").click()
        tr = find_Eles(driver, By.CSS_SELECTOR, ".table-list>table>tbody>tr")
        print len(tr)
        i = 0
        for ele in tr:
            try:
                i = i + 1
                find_Ele(driver, By.CSS_SELECTOR, "tbody>tr:nth-child(" + str(i) + ")>td>a:nth-child(2)").click()
                val = find_Ele(driver, By.ID, "title").get_attribute("value")
                print val
                find_Ele(driver, By.CSS_SELECTOR, ".packs+input").click()
                driver.switch_to.default_content()
                driver.switch_to.frame("Openadd")
                find_Ele(driver, By.CSS_SELECTOR, ".search_form>input").send_keys(replace_space(val))
                find_Ele(driver, By.CSS_SELECTOR, "#search").click()
                time.sleep(1)
                li = find_Eles(driver, By.CSS_SELECTOR, ".pack_list>ul>li")
                # print li
                if len(li) == 1:
                    find_Ele(driver, By.CSS_SELECTOR, ".pack_list>ul>li").click()
                elif len(li) > 1:
                    n = 0
                    for ele in li:
                        n = n + 1
                        element = driver.find_element_by_css_selector(
                            ".pack_list>ul>li:nth-child(" + str(n) + ")>input")
                        # element = find_Ele(driver, By.CSS_SELECTOR, ".pack_list>ul>li:nth-child(" + str(n) + ")>input")
                        print element.get_attribute("value")
                        if element.get_attribute("value") == replace_space(val):
                            ele.click()
                driver.switch_to.default_content()
                find_Ele(driver, By.CSS_SELECTOR, ".aui_state_highlight").click()
                time.sleep(1)
                driver.switch_to.frame("right")
                find_Ele(driver, By.NAME, "dosubmit").click()
            except Exception as err:
                print(err)


mydb = MysqldbHelper(host='localhost', port=3306, user='root', password='root', db='filmora')

# 配置多语言
def packRecurse_edit_ui(driver):
    if v_cookie(driver):
        print "cookie文件已经存在"
        use_cookies(driver)
    else:
        login(driver)
        save_cookies(driver)
    find_Ele(driver, By.ID, "_M497").click()
    time.sleep(0.5)
    if "block" in driver.find_element_by_css_selector("ul.page-sidebar-menu>li:nth-child(5)>ul").get_attribute("style"):
        find_Ele(driver, By.ID, "_MP561").click()
    else:
        find_Ele(driver, By.CSS_SELECTOR, "ul.page-sidebar-menu>li:nth-child(5)>a").click()
        find_Ele(driver, By.ID, "_MP561").click()
    driver.switch_to.frame("right")
    s1 = Select(driver.find_element_by_name("list_rows_select"))
    s1.select_by_value('100')
    for j in range(2, 10, 1):
        # time.sleep(1000)
        if j > 1 and j < 6 :
            find_Ele(driver, By.XPATH, "//li/a[contains(text(),'" + str(j) + "')]").click()
        elif j > 6:
            send_key(driver, str(j), By.CSS_SELECTOR, "#jump_to_input")
            find_Ele(driver, By.CSS_SELECTOR, "#jump_to_a").click()
        tr = find_Eles(driver, By.CSS_SELECTOR, ".table-list>table>tbody>tr")
        print len(tr)
        i = 76
        for ele in tr:
            try:
                i = i + 1
                find_Ele(driver, By.CSS_SELECTOR, "tbody>tr:nth-child(" + str(i) + ")>td>a").click()
                val = find_Ele(driver, By.ID, "v_en").get_attribute("value")
                print val," 第{}页，第{}个".format(j,i)
                res = exce_pack9_multi_language(val)
                if res is not None:
                    send_key(driver, res["fr"], By.NAME, "info[title][fr]")
                    send_key(driver, res["de"], By.NAME, "info[title][de]")
                    send_key(driver, res["jp"], By.NAME, "info[title][jp]")
                    send_key(driver, res["es"], By.NAME, "info[title][es]")
                    send_key(driver, res["it"], By.NAME, "info[title][it]")
                    send_key(driver, res["pt"], By.NAME, "info[title][pt]")
                    find_Ele(driver, By.NAME, "dosubmit").click()
                    mydb.executeCommentSqlOnce(
                        'UPDATE pack9_multi_language SET `status` = 1 WHERE en = \"{}\"'.format(val))
                else:
                    driver.back()
                    time.sleep(0.2)
                    driver.switch_to.frame("right")
                    # time.sleep(0.2)
                    # find_Ele(driver, By.NAME, "dosubmit").click()
                    print 'SELECT fr,de,es,it,pt,jp FROM pack9_multi_language WHERE binary en = \"{}\"'.format(
                        val) + " 结果为空"
            except Exception as err:
                print(err)
                mydb.executeCommentSqlOnce('UPDATE pack9_multi_language SET `status` = 2 WHERE en = \"{}\"'.format(val))
            finally:
                send_key(driver,str(j),By.CSS_SELECTOR,"#jump_to_input")
                find_Ele(driver, By.CSS_SELECTOR, "#jump_to_a").click()
                # find_Ele(driver, By.XPATH, "//li/a[contains(text(),'" + str(j) + "')]").click()


def exce_pack9_multi_language(name):
    # name = unicode(name, "utf-8")
    result = mydb.executeSqlOne(
        'SELECT fr,de,es,it,pt,jp FROM pack9_multi_language WHERE binary en = \"{}\"'.format(name))
    return result


def packRecurse_select_ui(driver):
    find_Ele(driver, By.CSS_SELECTOR, ".subnav>button").click()



def v_preElement(loc):
    if loc[0].lower() == 'id':
        preElement = EC.presence_of_element_located((By.ID, loc[1]))
    elif loc[0].lower() == "css":
        preElement = EC.presence_of_element_located((By.CSS_SELECTOR, loc[1]))
    elif loc[0].lower() == "xpath":
        preElement = EC.presence_of_element_located((By.XPATH, loc[1]))
    elif loc[0].lower() == "classname":
        preElement = EC.presence_of_element_located((By.CLASS_NAME, loc[1]))
    else:
        preElement = EC.presence_of_element_located((By.XPATH, ".//*[contains(@text,'" + loc[1] + "')]"))
    return preElement

    # 验证查询到传入的element


def find_ele_moreTimes(driver, index, loc, i=0):
    j = 5
    ele = find_Ele(driver, By.XPATH, "//li/a[contains(text(),'" + str(index) + "')]")
    if (i < 3):
        try:
            preElement = v_preElement(loc)
            WebDriverWait(driver, 5).until(preElement)
            ele.click(loc)
        except:
            i = i + 1
            find_Ele(driver, By.XPATH, "//li/a[contains(text(),'" + str(j) + "')]").click()
            j = j + 2
            find_ele_moreTimes(loc, index, i)
    else:
        print ("界面不存在")
        raise Exception("界面不存在")


if __name__ == "__main__":
    pass
    # exce_pack9_multi_language("wang")
    print get_now()
    url = "http://filmoraoa.wondershare.cn/Index"
    driver = get_driver()
    driver.get(url)
    driver.implicitly_wait(30)

    pack_ui(driver)
    # packRecurse_select_ui(driver)

    # driver.quit()
    # print get_now()
