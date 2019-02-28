# -*- coding: utf-8 -*-
import csv
import random
import socket
import sys
import ssl
import time
import requests
import threading
import http.client
import urllib.request
from retrying import retry
from setting import *
from bs4 import BeautifulSoup
from path.file_path import *


def get_proxy_list(targeturl):
    """获取代理网站"""
    global count_num
    for page in range(start_page, stop_page):
        get_page(page, targeturl, proxy_file)
        time.sleep(sleep_time)
    proxy_file.close()
    return count_num


def get_page(page, targeturl, proxy_file):
    """整理url，调用获取网页方法"""
    url = targeturl + str(page)
    print(url)
    ip_pool = built_ip_pool()
    html_data = parse_url_use_proxy(ip_pool, url)
    write_data(html_data, proxy_file)


def parse_url(url):
    """解析url， 返回请求网页字节流(已淘汰)"""
    request = urllib.request.Request(url, headers=requestHeader)
    html_data = urllib.request.urlopen(request).read()
    return html_data


def built_ip_pool():
    """构建代理池"""
    try:
        context = ip_csv.read()  # 读取成str
        results = context.split("\n")  # 以回车符\n分割成单独的行
        # 每一行的各个元素是以【,】分割的，因此可以
        length = len(results)
        list_result = []
        for n in range(length - 1):
            ip_port = results[n].split(",")[1:3]
            # print(ip_port)
            list_result.append(':'.join(ip_port))
            # print(list_result)
        return list_result
    except Exception as e:
        print("文件读取转换失败，请检查文件路径及文件编码是否正确")
        print(e)


@retry()
def parse_url_use_proxy(ip_pool, url):
    """
        parse_url3.0版
        设置代理
        失败重试（重点功能，踏破铁鞋无觅处）
        设置超时
    """
    proxy_addr = random.choice(ip_pool)
    print(requestHeader)
    url = urllib.request.Request(url, headers=requestHeader)
    # 使用代理请求
    print("--------以:http://%s 请求--------" % proxy_addr)
    # 使用urllib.request.ProxyHandler()设置代理服务器信息
    proxy = urllib.request.ProxyHandler({'http': 'http://' + proxy_addr})
    # 创建全局默认opener对象使urlopen()使用opener
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    # html_data = urllib.request.urlopen(url).read()
    html_data = urllib.request.urlopen(url, timeout=2).read()
    # print(html_data)
    return html_data


def write_data(html_data, proxyFile):
    """将爬取内容写入预存储文件"""
    global count_num
    soup = BeautifulSoup(html_data, "html.parser")
    # print(soup)
    trs = soup.find('table', id='ip_list').find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
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
        check_time = tds[8].text.strip()

        proxyFile.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (nation, ip, port, locate, anony, protocol, speed, check_time))
        # print('%s=%s:%s' % (protocol, ip, port))
        count_num += 1


def verify_proxy_list():
    """验证代理的有效性"""
    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0:
            break
        line = ll.strip().split(',')
        # protocol = line[5]
        ip = line[1]
        port = line[2]

        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5.0)
            conn.request(method='GET', url=check_url, headers=requestHeader)
            # res = conn.getresponse()
            lock.acquire()
            print("+++Success:" + ip + ":" + port)
            outFile.write(ll + "\n")
            lock.release()
        except Exception as e:
            print("---Failure:" + ip + ":" + port)
            if e:
                pass


def choose_proxy():
    """选择代理属性"""
    print("代理来源:以逗号分隔, 取消请回车(直接验证本地代理)")
    print("1:国内高匿")
    print("2:国内透明")
    print("3:国外高匿")
    print("4:国外透明")
    chooses = input("请输入:").split(',')
    if not chooses:
        pass
    else:
        if chooses == ['0']:
            chooses = ['1', '2', '3', '4']
        for choose in chooses:
            if choose == "1":
                proxynum = get_proxy_list("http://www.xicidaili.com/nn/")
                print(u"国内高匿：" + str(proxynum))
            elif choose == "2":
                proxynum = get_proxy_list("http://www.xicidaili.com/nt/")
                print(u"国内透明：" + str(proxynum))
            elif choose == "3":
                proxynum = get_proxy_list("http://www.xicidaili.com/wn/")
                print(u"国外高匿：" + str(proxynum))
            elif choose == "4":
                proxynum = get_proxy_list("http://www.xicidaili.com/wt/")
                print(u"国外透明：" + str(proxynum))


def check_proxy():
    """验证代理的有效性"""
    print(u"\n验证代理的有效性：")
    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verify_proxy_list)
        all_thread.append(t)
        t.start()
    for t in all_thread:
        t.join()


def clean():
    """清理内存"""
    inFile.close()
    outFile.close()
    ip_csv.close()
    print("All Done.")


# noinspection PyGlobalUndefined
def before_everything():
    """创建或打开文件， 调用配置信息"""
    global inFile, outFile, ip_csv, check_url, proxy_file
    inFile = open(infile_path)
    outFile = open(outfile_path, 'w')
    proxy_file = open(infile_path, 'a')

    ip_csv = open('user_proxies.csv', 'r', encoding="utf-8")


if __name__ == '__main__':
    before_everything()
    choose_proxy()
    check_proxy()
    clean()
