from bs4 import BeautifulSoup
from httpproxy import *

# 暂时处理ssl受信问题
ssl._create_default_https_context = ssl._create_unverified_context

__author__ = 'cooper'

lock = threading.Lock()

countNum = 0
requestHeader = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}


TARGET_URL= "http://www.xicidaili.com/nn/"