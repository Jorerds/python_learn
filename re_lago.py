import urllib.request
from lxml import etree
import json
import requests
import time
import re

def re_lag():
    url_start = "https://www.lagou.com/jobs/list_运维?labelWords=&fromSearch=true&suginput="
    url_parse = "https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?labelWords=&fromSearch=true&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    L = []
    dis=[]
    for x in range(1, 30):
        data = {
            'first': 'true',
            'pn': str(x),
            'kd': '运维'
        }
        s = requests.Session()
        s.get(url_start, headers=headers, timeout=3)  # 请求首页获取cookies
        cookie = s.cookies  # 为此次获取的cookies
        response = s.post(url_parse, data=data, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
        time.sleep(3)
        response.encoding = response.apparent_encoding
        text = json.loads(response.text)
        for urls in text['content']['hrInfoMap']:
            L.append(urls)
    print(L)
    for i in L:
        html=re_info(int(i))
        for a in html:
            if re.findall(r'培训', a):
                dis.append(i)
    print(set(dis))

def re_info(uid):
    url = "https://www.lagou.com/jobs/%s.html"%uid
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?labelWords=&fromSearch=true&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    res = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(res)
    data = html.read().decode('utf-8')
    datas=etree.HTML(data)
    nifo = datas.xpath('//*[@class="job-detail"]/p/text()')
    return nifo
    
if __name__ == '__main__':
  re_lag()
