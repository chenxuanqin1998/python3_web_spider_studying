#!/usr/bin/env python
# coding: utf-8

# In[71]:


import json
import requests
from requests.exceptions import RequestException
import time

from lxml import etree

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


# In[72]:


def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')


# In[73]:


def parse_one_page(text):
    html = etree.HTML(text)
    result_title = html.xpath('//dl[@class="board-wrapper"]/dd/a/@title')
    result_index = html.xpath('//dl[@class="board-wrapper"]/dd/i/text()')
    result_original_actor = html.xpath('//dl[@class="board-wrapper"]/dd//p[@class="star"]/text()')
    result_actor = [actor.strip() for actor in result_original_actor]
    result_original_time = html.xpath('//dl[@class="board-wrapper"]/dd//p[@class="releasetime"]/text()')
    result_time = [data.strip()[5:].strip() for data in result_original_time]
    result_sorce_integer = html.xpath('//dl[@class="board-wrapper"]/dd//p[@class="score"]/i[@class="integer"]/text()') 
    result_sorce_fraction = html.xpath('//dl[@class="board-wrapper"]/dd//p[@class="score"]/i[@class="fraction"]/text()')
    result_sorce = list(zip(result_sorce_integer,result_sorce_fraction))
    result = list(zip(result_title,result_index,result_actor,result_time, result_sorce))
    write_to_file(result)


# In[74]:


def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    parse_one_page(html)


# In[75]:


for i in range(10):
    main(offset=i*10)
    time.sleep(1)

