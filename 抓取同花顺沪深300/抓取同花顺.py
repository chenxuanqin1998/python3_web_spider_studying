#!/usr/bin/env python
# coding: utf-8

# In[24]:


import json
import requests
from requests.exceptions import RequestException
import re
import time


# In[25]:


def get_one_page(url):
    try:
        headers = {
            "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/71.0.3578.98 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            response.encoding = 'gbk'
            return response.text
        else:
            return None
    except RequestException:
        return None


# In[26]:


def parse_one_page(html):
    pattern = re.compile('<head>.*?<title>(.*?)最新动态.*?id="dtsyl">(.*?)</span>.*?每股收益.*?class="tip f12">(.*?)</span>'
                         + '.*?id="jtsyl">(.*?)</span>.*?id="sjl">(.*?)</span>.*?每股净资产'
                         + '.*?"tip f12">(.*?)</span>.*?净资产收益率.*?"tip f12">(.*?)</span>', re.S)
    items = re.search(pattern,html)
    return items


# In[27]:


def main(sign):
    url = 'http://basic.10jqka.com.cn/'+str(sign)
    html = get_one_page(url)
#    print(html)
    items = parse_one_page(html)
    store_data(items)


# In[28]:


def store_data(items):
    dic = {}
    dic['name'] = items.group(1)
    dic['dtsyl'] = items.group(2)
    dic['mgsy'] = items.group(3)
    dic['jtsyl'] = items.group(4)
    dic['sjl'] = items.group(5)
    dic['mgjzc'] = items.group(6)
    dic['jzcsyl'] = items.group(7)
    write_to_file(dic)


# In[29]:


def write_to_file(content):
    with open('tonghuasun_result.txt','a',encoding='gbk') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')


# In[30]:


with open('沪深300.json') as f:
    sign_data = json.load(f)
for sign in sign_data:
    main(sign)
#time.sleep(1)


# In[31]:


#url = 'http://basic.10jqka.com.cn/000651'
#html = get_one_page(url)
#print(html)

