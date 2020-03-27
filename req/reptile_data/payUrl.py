import urllib2
import os, re


def url_open(url):
    res = urllib2.Request(url)
    res.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36")
    response = urllib2.urlopen(res)
    html = response.read()
    for h in response.info().headers:
        print h
    # print response.info().headers
    # print ''.join(response.info().headers)
    return html


def get_page(url):
    html = url_open(url).decode("utf-8")
    # print(html)
    begin = html.find('<main')
    end = html.find('main>', begin)
    return html[begin:end]


def find_payUrl(page_url):
    html = url_open(page_url).decode("utf-8")
    # print(html)
    ima_addrs = []
    begin = html.find('img src=')
    while begin != -1:
        end = html.find('.jpg', begin, begin + 255)
        # print(html[begin:end])
        if end != -1:
            ima_addrs.append(html[begin + 9:end + 4])
        else:
            end = begin + 9
        begin = html.find('img src=', end)
    print(ima_addrs)
    return ima_addrs


if __name__ == '__main__':
    url_open("https://effects.wondershare.com")
