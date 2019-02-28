from httpproxy import *

# 更改配置信息
start_page = 1
stop_page = 2
sleep_time = 3
# proxy = input("是否使用代理（0，1）")


# 暂时处理ssl受信问题
ssl._create_default_https_context = ssl._create_unverified_context

# 创建锁
lock = threading.Lock()

# 创建文件
tmp = open(infile_path, 'w')
tmp.write("")
tmp.close()

# 设置代理信息
USER_AGENT = [
            {'User-agent': 'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'},
            {'User-agent': 'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'},
            {'User-agent': 'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)'},
            {'User-agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1'},
            {'User-agent': 'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1'},
            {'User-agent': 'Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11'},
            {'User-agent': 'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11'},
            {'User-agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TheWorld)'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;AvantBrowser)'},
            {'User-agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)'},
        ]
requestHeader = random.choice(USER_AGENT)

# 设置临时变量
count_num = 0

# 设置常量
__author__ = 'cooper'
TARGET_URL = "http://www.xicidaili.com/nn/"
check_url = 'http://www.baidu.com/'
