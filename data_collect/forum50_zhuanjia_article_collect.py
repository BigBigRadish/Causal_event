# -*- coding: utf-8 -*-
'''
Created on 2018年11月11日

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
from threading import Thread
user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers={'User-Agent':user_agent}
requests.adapters.DEFAULT_RETRIES = 5
def crawl_forum50_article(lanmu,collection):
    mu = threading.Lock()
    for i in lanmu:
        lanmu_url='http://www.50forum.org.cn/home/article/lists/category/'+i+'.html'
        html=requests.get(lanmu_url,headers=headers,verify=False)
        soup1=BeautifulSoup(html.content,"lxml",from_encoding='utf-8')
        if(soup1.find(class_='end')!=None):
            page=int(soup1.find(class_='end').text)#可以显示到10，10以后才会有end
        else:
            page=int(soup1.find(class_='num').text)
        for j in range(page):
            page_url='http://www.50forum.org.cn/home/article/lists/category/'+str(i)+'/p/'+str(j)+'.html'#爬取每个版面的主目录
            html1=requests.get(page_url,headers=headers,verify=False)
            soup=BeautifulSoup(html1.content,"lxml",from_encoding='utf-8')
            article=soup.find(class_='list_list mtop10').findAll('a')
            if article != None:
                for k in article:
                    title=k['title']#文章标题
                    article_url='http://www.50forum.org.cn'+str(k['href'])#文章链接
                    f=codecs.open(str('E:/Causal_events/forum50_articles/'+str(title).replace(':','').replace('"','').replace('+','').replace('*','').replace('：','').replace('?','').replace('十','').replace(' ','')+'.txt'),'a','utf-8')#标题去除异常字符
                    html2=requests.get(article_url,headers=headers,verify=False)
                    soup2=BeautifulSoup(html2.content,"lxml",from_encoding='utf-8')
                    #print(soup2.text)
                    content=soup2.findAll('p')#文章内容
                    content1=''
                    for l in content:
                        content1+=str(l.text).strip().replace('\xa0', '').replace('\t', '').replace(' ', '')
                    #print(content1) #文章内容  
                    if  mu.acquire(True): #确保文件写入成功
                        f.write(content1)
                        f.flush()
                        os.fsync(f)
                        f.close()
                        mu.release()
                    if soup2.findAll('div', class_='list_content_title')!=None:
                        content_title=str(soup2.findAll('div', class_='list_content_title')[1].text)#标题内容
                        
                        #print(content_title)
                        content_title=content_title.strip()
                        content_title=content_title.replace('\xa0\xa0', ',').replace('\t', '').replace('    ', '')#替换空格字符及其制表符
                        author=content_title.split(',')[0].split('：')[1]#作者
                        print(author)
                        work_place=content_title.split(',')[1].split('：')[1]#工作单位
                        publish_time=content_title.split(',')[2].split('：')[1]#发布时间
                        try:
                            read_times=content_title.split(',')[3].split('：')[0]#阅读次数
                        except: 
                            read_times='无'
                        article_Detail={'栏目':i,'文章标题':title,'作者':author,'工作单位':work_place,'发布时间':publish_time,'阅读次数':read_times,'文章内容':content1}
                        collection.insert(article_Detail)
if __name__ == '__main__':
    mongo_con=MongoClient('172.20.66.56', 27017)
    db=mongo_con.Causal_event
    collection=db.forum_articles_50
    lanmu=['hongguanjingji','tizhigaige','sannongwenti','chanyejingji','jinrong','jiuye','zhuanjiaqita']#宏观经济，体制改革，三农问题，产业经济，金融与外贸，人口与就业，其他               
    crawl_forum50_article(lanmu,collection)
    db.close()            
            
            
        
    