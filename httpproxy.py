# -*- coding: utf-8 -*-
import sys
import ssl
import time
import requests
import threading
import http.client
import urllib.request
from setting import *
from bs4 import BeautifulSoup


# version control
# if sys.version_info < (3, 0):   # 如果小于Python3
#     PYTHON_3 = False
# else:
#     PYTHON_3 = True
# 
# if not PYTHON_3:   # 如果小于Python3
#     reload(sys)
#     sys.setdefaultencoding("utf-8")
inFile = open('proxy.txt')
outFile = open('verified.txt', 'w')

def parse_page(line, proxyFile):
    global countNum
    tds = line.find_all('td')
    # 国家
    if tds[0].find('img') is None:
        nation = '未知'
        locate = '未知'
    else:
        nation = tds[0].find('img')['alt'].strip()
        locate = tds[3].text.strip()
    ip = tds[1].text.strip()
    port = tds[2].text.strip()
    anony = tds[4].text.strip()
    protocol = tds[5].text.strip()
    speed = tds[6].find('div')['title'].strip()
    time = tds[8].text.strip()

    proxyFile.write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (nation, ip, port, locate, anony, protocol, speed, time))
    # print('%s=%s:%s' % (protocol, ip, port))
    countNum += 1


def get_page(page, targeturl, proxyFile):
    url = targeturl + str(page)
    # print(url)
    request = urllib.request.Request(url, headers=requestHeader)
    html_doc = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    # print(soup)
    trs = soup.find('table', id='ip_list').find_all('tr')
    for tr in trs[1:]:
        parse_page(tr, proxyFile)


def getProxyList(targeturl):
    global countNum
    proxyFile = open('./data/proxy.txt', 'a')

    for page in range(1, 2):
        get_page(page, targeturl, proxyFile)
        time.sleep(1)

    proxyFile.close()
    return countNum


def verifyProxyList():
    '''
    验证代理的有效性
    '''
    requestHeader = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    check_url = 'http://www.baidu.com/'

    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0: break
        line = ll.strip().split('|')
        protocol = line[5]
        ip = line[1]
        port = line[2]

        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5.0)
            conn.request(method='GET', url=check_url, headers=requestHeader)
            res = conn.getresponse()
            lock.acquire()
            print("+++Success:" + ip + ":" + port)
            outFile.write(ll + "\n")
            lock.release()
        except Exception as e:
            print("---Failure:" + ip + ":" + port)
            if e:
                pass


if __name__ == '__main__':
    tmp = open('proxy.txt', 'w')
    tmp.write("")
    tmp.close()
    proxynum = getProxyList("http://www.xicidaili.com/nn/")
    print(u"国内高匿：" + str(proxynum))
    proxynum = getProxyList("http://www.xicidaili.com/nt/")
    print(u"国内透明：" + str(proxynum))
    proxynum = getProxyList("http://www.xicidaili.com/wn/")
    print(u"国外高匿：" + str(proxynum))
    proxynum = getProxyList("http://www.xicidaili.com/wt/")
    print(u"国外透明：" + str(proxynum))

    print(u"\n验证代理的有效性：")

    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()

    for t in all_thread:
        t.join()

    inFile.close()
    outFile.close()
    print("All Done.")
