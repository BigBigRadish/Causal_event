# -*- coding: utf-8 -*-
'''
Created on 2018年11月12日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import requests
import logging 
import urllib.request;
import time
import random
import json
import re
import urllib.request
import redis
import pymysql 
import itertools
from pymongo import MongoClient
from http import cookiejar
import codecs
import os
user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers={'User-Agent':user_agent}
requests.adapters.DEFAULT_RETRIES = 5
mu = threading.Lock()
def craw_sina_finance_articles(collection):
    for i in range(1,22):
        sina_url='http://finance.sina.com.cn/roll/index.d.html?cid=57565&page'+str(i)
        logging.captureWarnings(True)
    #     r = requests.get(sina_url,headers=headers,verify=False)
    #     _cookies=r.cookies#获取cookie
        html=requests.get(sina_url,headers=headers,verify=False);
        html.raise_for_status()
        #print(html.text)
        soup=BeautifulSoup(html.content,"lxml",from_encoding='utf-8')
        li=soup.findAll("li")
        for j in li[2:]:
            article_url=j.findAll('a')[0]['href']#文章链接
            article_title=j.findAll('a')[0].text#文章标题
            author=j.findAll('a')[1].text#文章作者
            publish_time=j.find('span').text.replace('(','').replace(')','')#发表时间
            f=codecs.open(str('E:/Causal_events/sina_economics_articles/'+str(article_title).replace(':','').replace('"','').replace('+','').replace('*','').replace('：','').replace('?','').replace(' ','')+'.txt'),'a','utf-8')#标题去除异常字符
            #print(article_title,article_url,author,publish_time)
            r = requests.get(article_url,headers=headers,verify=False)
            soup1=BeautifulSoup(r.content,"lxml",from_encoding='utf-8')
            content=soup1.find(class_="articalContent")
            article_content=content.text.strip().replace('\t','').replace('\n','').replace(' ','').replace('阅读┊收藏┊转载┊喜欢▼┊打印┊举报','').replace('免责声明：博主所发内容不构成买卖股票依据。股市有风险，入市需谨慎。新浪财经网站提供此互动平台不代表认可其观点。新浪财经所有博主不提供代客理财等非法业务。有私下进行收费咨询或推销其他产品服务，属于非法个人行为，与新浪财经无关，请各位网友务必不要上当受骗！查看博主原文>>@@title@@@@teacher_name@@：@@title@@0转载喜欢','').replace('\r','')
            if  mu.acquire(True): #确保文件写入成功
                f.write(content)
                f.flush()
                os.fsync(f)
                f.close()
                mu.release()
            article_Detail={'文章标题':article_title,'文章作者':author,'文章链接':article_url,'文章内容':article_content,'发表时间':publish_time}
            collection.insert(article_Detail)
if __name__ == '__main__':
    mongo_con=MongoClient('172.20.66.56', 27017)
    db=mongo_con.Causal_event
    collection=db.sina_ecomics_articles
    craw_sina_finance_articles(collection)
    db.close()
        
        
        
    