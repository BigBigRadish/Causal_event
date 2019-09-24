'''
Created on 2019年9月24日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#爬取中国经济网
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
def crawl_forum50_article(lanmu):
#     mu = threading.Lock()
    for i in lanmu:
        bankuai=i.split('/')[4]#栏目
        for j in range(0,17):
            if j!=0:
                lanmu_url=i.replace('index','index'+'_'+str(j))
            else:lanmu_url=i
            lanmu_html=requests.get(lanmu_url,headers=headers,verify=False)
            soup1=BeautifulSoup(lanmu_html.content,"lxml",from_encoding='utf-8')
#             print(soup1)
            if soup1.find(class_='neirong'):
                pages_content=soup1.find(class_='neirong').findAll('li')#每一页的总文章
            else:
                break
            for article_detail in pages_content:
                article_href=article_detail.a['href']
#                 print(article_href)
                article_title=article_detail.a.text.replace('\n','')#文章标题
                article_title= re.sub(r'[^\w\s]','_',article_title.replace(' ',''))#所有标点符号替换成_
#                 print(article_title)
                try:
                    article_html=requests.get(article_href,headers=headers,verify=False)
                except Exception:
                    continue    
                soup2=BeautifulSoup(article_html.content,"lxml",from_encoding='utf-8')
#                 print(soup2)
                print(article_title)
                try:
                    article_content=soup2.find('div',class_="TRS_Editor").text
                except Exception:
                    continue
                                    
                with codecs.open('E:/Causal_events/finance_ce/'+bankuai+'/'+article_title+'.txt','a','utf-8') as f:#标题去除异常字符
                    f.write(article_content)
if __name__ == '__main__':
#     mongo_con=MongoClient('172.20.66.56', 27017)
#     db=mongo_con.Causal_event
#     collection=db.forum_articles_50
    lanmu=['http://views.ce.cn/main/net/index.shtml',\
           'http://views.ce.cn/fun/who/index.shtml',\
           'http://views.ce.cn/view/economy/index.shtml',\
           'http://views.ce.cn/view/obs/index.shtml',\
           'http://views.ce.cn/view/society/index.shtml',\
           'http://views.ce.cn/main/zt/index.shtml']#专题,经济大讲堂,观察家,经济眼,经济学人,声音
    crawl_forum50_article(lanmu)
#     mongo_con.close() #关闭连接   
