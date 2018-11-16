# -*- coding: utf-8 -*-
'''
Created on 2018年11月13日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import selenium
from bs4 import BeautifulSoup#引入beautifulsoup加快解析速度
from PIL import Image,ImageEnhance
from selenium import  webdriver
import pytesser3
import pytesseract
import time
import re
from pdfminer.pdfparser import PDFParser,PDFDocument
from pymongo import MongoClient
from selenium.webdriver.support.select import Select
from selenium import webdriver 
from io import StringIO
import os
#os.environ["webdriver.chrome.driver"] = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
tessdata_dir_config = '--tessdata-dir "D:\\tesseract-ocr\\tessdata"'#tessdata
pytesseract.pytesseract.tesseract_cmd = 'D:\\tesseract-ocr\\tesseract.exe'#tesseract.exe路径
def get_auth_code(driver,codeEelement):
    '''获取验证码'''
    driver.save_screenshot('./login.png')  #截取登录页面
    imgSize = codeEelement.size   #获取验证码图片的大小
    imgLocation = imgElement.location #获取验证码元素坐标
    rangle = (int(imgLocation['x']),int(imgLocation['y']),int(imgLocation['x'] + imgSize['width']),int(imgLocation['y']+imgSize['height']))  #计算验证码整体坐标
    login = Image.open("./login.png")  
    frame4=login.crop(rangle)   #截取验证码图片
    frame4.save('./authcode.png')
    authcodeImg = Image.open('./authcode.png')
    authCodeText = pytesseract.image_to_string(authcodeImg,config=tessdata_dir_config).strip().replace(' ','')
    print(authCodeText)
    return authCodeText

def newone_login(driver,account,passwd,authCode):
    '''登录招商证券系统'''
    driver.find_element_by_id('username').send_keys(account)#用户名
    driver.find_element_by_id('password').send_keys(passwd)#密码
    driver.find_element_by_id('code').send_keys(authCode)#验证码
    driver.find_element_by_id('loginBtn').click()
    time.sleep(2)
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
        
        for j in article_detail[0:]:
#             n=0
#             n+=1
#             print('n:'+str(n))
            href=j.find('a')['href']#得到后缀链接
            publish_date=j.find('em').text#得到日期
            article_href.append(href+','+publish_date)
        
        for k in article_href:
#             m+=1
#             print('m:'+str(m))
            article_url=k.split(',')[0]#文章后缀链接
            article_publish_time=k.split(',')[1]#文章发表时间
            driver.get('http://www.newone.com.cn'+article_url)
            content1=driver.page_source.encode('utf-8')
            soup1= BeautifulSoup(content1, 'lxml')#文章内容，包括pdf链接
            title=soup1.find("h1").text#文章标题
            author=soup1.find(class_="pop_cont").findAll('td')[1].text#文章作者
            if soup1.find('span',style="color:#a2162e;font-size:16px;font-weight:bold").find('a')!=None:
                article_name=soup1.find('span',style="color:#a2162e;font-size:16px;font-weight:bold").find('a').text#文章名
                article_pdf_url=soup1.find('span',style="color:#a2162e;font-size:16px;font-weight:bold").find('a')['href']#文章后缀链接
                pdf_article.append(article_pdf_url)
                article_info={'报告类型':lanmu,'文章页码':i,'发表日期':article_publish_time,'文章链接':'http://www.newone.com.cn'+article_url,'文章标题':title,'文章作者':author,'pdf文件名':article_name,'pdf链接':article_pdf_url}
                collection.insert(article_info)
            else:
                continue
            #print(m)
            
        driver.get('http://www.newone.com.cn/researchcontroller/search')
        selector = Select(driver.find_element_by_tag_name('select'))
        selector.select_by_visible_text(lanmu)        
        time.sleep(1)
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
    driver.get('https://www.newone.com.cn/nwsecure/login_jiaoyi')#打开登陆网站
    driver.maximize_window()
    time.sleep(30)#设置一下，自动保存文件
    imgElement = driver.find_element_by_id('codeimg')#获取图片元素
    authCodeText = get_auth_code(driver,imgElement)
    newone_login(driver,'1808494215','681218',authCodeText)
    article_lanmu=['宏观研究','策略研究','行业研究','招商视点','公司研究']
    for lanmu in article_lanmu:
        crawl_articles_detail(driver,collection,lanmu)
    #print(driver.get_cookies())#获取到cookies了
    #driver.get('http://www.newone.com.cn/researchcontroller/detail?id=227696')
    mongo_con.close()
    driver.quit()

