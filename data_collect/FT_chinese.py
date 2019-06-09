# -*- coding: utf-8 -*-
'''
Created on 2019年6月9日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#爬取金融时报中文网
import selenium
from bs4 import BeautifulSoup#引入beautifulsoup加快解析速度
from PIL import Image,ImageEnhance
from selenium import  webdriver

import time
import re
from pymongo import MongoClient
from selenium.webdriver.support.select import Select
from selenium import webdriver 
from io import StringIO
import requests
import os

def newone_login(driver,account,passwd,authCode):
    '''登陆FT中文网'''
    driver.find_element_by_id('email').send_keys(account)#用户名
    driver.find_element_by_id('password').send_keys(passwd)#密码
    driver.find_element_by_id('captchacode').send_keys(authCode)#验证码
    driver.find_element_by_css_selector("[type=submit]").click()
#     time.sleep(2)
def crawl_articles_detail(driver,collection,lanmu):
    pdf_article=[]#存储所有的文章的pdf版链接
    article_href=[]#存储所有文章链接
    driver.get('http://www.newone.com.cn/researchcontroller/search')
    selector = Select(driver.find_element_by_tag_name('select'))
    selector.select_by_visible_text(lanmu)
#     js = 'document.getElementById("tempsj").removeAttribute("readonly");'
#     driver.execute_script(js)
#     js_value = 'document.getElementById("tempsj").value="20050901"'
#     driver.execute_script(js_value)
#     js = 'document.getElementById("tempsj2").removeAttribute("readonly");'
#     driver.execute_script(js)
#     js_value = 'document.getElementById("tempsj2").value="20180904"'
#     driver.execute_script(js_value)
    driver.find_element_by_name('B1').click()
    page_text=driver.find_element_by_xpath('//td[@width="72"]').text#获取总页码信息
    page=int(re.findall('/ (.*)页',page_text)[0])
    #print(str(page))
    for i in range(1,page):#2370篇，158页
        print("i:"+str(i))
    #driver.find_element_by_xpath('//a[@href="javascript:gopage(4);"]').click()
        driver.execute_script("gopage("+str(i)+")")#翻页
        content=driver.page_source.encode('utf-8')
        soup = BeautifulSoup(content, 'lxml')#试用beautifulsoup解析
        article_detail=soup.find(id="td5").findAll('li')
        #存储所有的文章链接+发表时间
        n=0
        for j in article_detail[0:]:
            n+=1
            print('n:'+str(n))
            href=j.find('a')['href']#得到后缀链接
            publish_date=j.find('em').text#得到日期
            article_href.append(href+','+publish_date)
        driver.get('http://www.newone.com.cn/researchcontroller/search')
        selector = Select(driver.find_element_by_tag_name('select'))
        selector.select_by_visible_text(lanmu)        
        time.sleep(1)
    m=0
    for k in article_href:
        m+=1
        print('m:'+str(m))
        article_url=k.split(',')[0]#文章后缀链接
        article_publish_time=k.split(',')[1]#文章发表时间
        driver.get('http://www.newone.com.cn'+article_url)
        content1=driver.page_source.encode('utf-8')
        soup1= BeautifulSoup(content1, 'lxml')#文章内容，包括pdf链接
        title=soup1.find("h1").text#文章标题
        author=soup1.find(class_="pop_cont").findAll('td')[1].text#文章作者
        if soup1.find('span',style="color:#a2162e;font-size:16px;font-weight:bold")!=None:
            if soup1.find('span',style="color:#a2162e;font-size:16px;font-weight:bold").find('a')!=None:
                article_name=soup1.find('span',style="color:#a2162e;font-size:16px;font-weight:bold").find('a').text#文章名
                article_pdf_url=soup1.find('span',style="color:#a2162e;font-size:16px;font-weight:bold").find('a')['href']#文章后缀链接
                pdf_article.append(article_pdf_url)
                article_info={'报告类型':lanmu,'发表日期':article_publish_time,'文章链接':'http://www.newone.com.cn'+article_url,'文章标题':title,'文章作者':author,'pdf文件名':article_name,'pdf链接':article_pdf_url}
#                 collection.insert(article_info)
            else:
                continue
        else:
            continue
        #print(m)
            
        
    for pdf_href in pdf_article: #保存文件，有问题
        #f=open('G:\\articles/1.pdf','wb')
        driver.get('http://www.newone.com.cn'+pdf_href)
        time.sleep(2)
        
        

if __name__ == '__main__':
    mongo_con=MongoClient('172.20.66.56', 27017)
    db=mongo_con.Causal_event
    collection=db.newone__articles
    options = webdriver.ChromeOptions() 
    prefs = {'download.default_directory': 'G:/articles/',"download.prompt_for_download": False}
    options.add_experimental_option('prefs', prefs) 
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('http://user.ftchinese.com/login')#打开登陆网站
    driver.maximize_window()
#     time.sleep(5)#设置一下，自动保存文件
    authCodeText=input()#验证码手动输入。。。
    newone_login(driver,'luozhukun@163.com','lzk15884706478',authCodeText)
    cookies=driver.get_cookies()
    cookie_dict={}
    for i in cookies:
        cookie_dict[i['name']]=i['value']
    print(cookie_dict)
    driver.add_cookie(cookie_dict)
    url='http://www.ftchinese.com/premium/001083082?topnav=economy&subnav=chinaeconomy'
    driver.get(url)
    content=driver.page_source.encode('utf-8')
    print(content)
#     driver.get('http://www.ftchinese.com/channel/economy.html')
    time.sleep(5)
    mongo_con.close()
    driver.quit()
