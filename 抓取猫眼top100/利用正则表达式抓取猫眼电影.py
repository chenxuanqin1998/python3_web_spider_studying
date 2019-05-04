#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import requests
from requests.exceptions import RequestException
import re
import time
def get_one_page(url):
    try:
        headers = {
            "User-Agent":'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/63.0.3239.132 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


# In[3]:


def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')


# In[4]:


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?title="(.*?)"'
                         + '.*?star">(.*?)</p>.*?releasetime'
                         + '.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern,html)
    for item in items:
        dic = {}
        dic['index'] = item[0]
        dic['image'] = item[1]
        dic['title'] = item[2].strip()
        dic['actor'] = item[3].strip()[3:] if len(item[3])> 3 else ''
        dic['time'] = item[4].strip()[5:].strip() if len(item[4]) > 5 else ''
        dic['score'] = item[5].strip()+item[6].strip()
        write_to_file(dic)
        print(dic)


# In[5]:


def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    parse_one_page(html)


# In[6]:


for i in range(10):
    main(offset=i*10)
    time.sleep(1)

