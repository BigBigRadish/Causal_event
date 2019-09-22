'''
Created on 2019年9月22日
@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#爬取证券时报国内，海外，深度，评论，时报，创投，专栏新闻
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import requests
from pymongo import MongoClient
import codecs
import os
import re
from zhon.hanzi import punctuation
from threading import Thread
user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers={'User-Agent':user_agent}
requests.adapters.DEFAULT_RETRIES = 5
def crawl_forum50_article(lanmu,collection):
    mu = threading.Lock()
    for i in lanmu:
        for j in range(1,21):
            lanmu_url='http://news.stcn.com/'+i+'/'+str(j)+'.shtml'
            lanmu_html=requests.get(lanmu_url,headers=headers,verify=False)
            soup1=BeautifulSoup(lanmu_html.content,"lxml",from_encoding='utf-8')
#             print(soup1)
            pages_content=soup1.findAll(class_='tit')#每一页的总文章
            for article_detail in pages_content:
                article_href=article_detail.a['href']
#                 print(article_href)
                article_title=article_detail.text#文章标题
                article_title= re.sub(r'[^\w\s]','_',article_title.replace(' ',''))#所有标点符号替换成_
#                 print(article_title)
                article_html=requests.get(article_href,headers=headers,verify=False)
                soup2=BeautifulSoup(article_html.content,"lxml",from_encoding='utf-8')
                article_content=soup2.find(class_='txt_con').text
                with codecs.open('E:/Causal_events/stcn/'+i+'/'+article_title+'.txt','a','utf-8') as f:#标题去除异常字符
                    f.write(article_content)
if __name__ == '__main__':
    mongo_con=MongoClient('172.20.66.56', 27017)
    db=mongo_con.Causal_event
    collection=db.forum_articles_50
    lanmu=['guonei','xwhw','sdbd','xwpl','sbgc','xwct']#国内，海外，深度，评论，时报，创投               
    crawl_forum50_article(lanmu,collection)
    mongo_con.close() #关闭连接           
            
            
        
    