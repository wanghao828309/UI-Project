import urllib.request
import os

def url_open(url):
    res = urllib.request.Request(url)
    res.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36")
    respone = urllib.request.urlopen(res)
    html = respone.read()
    return html

def get_page(url):
    html = url_open(url).decode("utf-8")
    # print(html)
    begin = html.find('Older Comments')+45
    end = html.find('#comments',begin)
    return html[begin:end]
    

def find_imgs(page_url):
    html = url_open(page_url).decode("utf-8")
    # print(html)
    ima_addrs = []
    begin = html.find('img src=')
    while begin != -1:
        end = html.find('.jpg',begin ,begin+255)
        # print(html[begin:end])
        if end != -1:
            ima_addrs.append(html[begin+9:end+4])
        else:
            end = begin + 9
        begin = html.find('img src=', end)
    print(ima_addrs)
    return  ima_addrs

def save_img(floder,img_addrs):
    for i in img_addrs:
        filename = i.split("/")[-1]
        url = i.replace(r"//i1.1100lu.xyz/1100/201805/05",r"http://i1.1100lu.xyz/1100/201805/05")
        with open(filename,'wb') as f:
            img = url_open(url)
            f.write(img)


def dowmload_jpg(url ,floder = "page" , page=5):
    os.mkdir(floder)
    os.chdir(floder)

    # page_num = int(get_page(url))
    page_num = 412903
    for i in range(page):
        page_num -= i
        # page_url = url + "page-"+ str(page_num) + "#comments"
        page_url = url + str(page_num) + ".html"
        print(page_url)
        img_addrs = find_imgs(page_url)
        save_img(floder,img_addrs)


if __name__ == '__main__':
    pass

    # find_imgs("http://jandan.net/ooxx/page-50689514#comments")
    # dowmload_jpg("http://9999av.vip/html/tupian/siwa/2018/0505/")



