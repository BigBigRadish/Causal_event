# -*- coding: utf-8 -*-
'''
Created on 2018年11月13日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import selenium
from PIL import Image,ImageEnhance
from selenium import  webdriver
import os
import pytesser3
import sys,time
#import tesserocr 
import requests
import logging
import pytesseract
from bs4 import BeautifulSoup
user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers={'User-Agent':user_agent}
requests.adapters.DEFAULT_RETRIES = 5
def get_randomId():
    firstUrl = "https://www.newone.com.cn/nwsecure/login_jiaoyi"
    html= requests.get(firstUrl,headers = headers,verify=False)
    soup=BeautifulSoup(html.content,"lxml",from_encoding='utf-8')
    print(soup)
    random_id=soup.find('input',id="randomID")['value']
    captua_url=soup.find('img',id="codeimg")['src']
    print(random_id)
    return random_id,captua_url
def login(par1):
    session = requests.Session()
    afterURL = "http://www.newone.com.cn/researchcontroller/detail?id=202376"        # 想要爬取的登录后的页面
    loginURL = "https://www.newone.com.cn/nwsecure/securecontroller/authenticate"     # POST发送到的网址
    res =session.post(loginURL,data=par1,headers=headers)
    response=session.get(afterURL,verify = False)
    print(res.content)
#     print(response.cookies)    # 获得登陆后的响应信息，使用之前的cookie
    return response.content
def captua_code(captua_url):
#     valcode = requests.get(captua_url)
#     f = open('./valcode.jpg', 'wb')
#     # 将response的二进制内容写入到文件中
#     f.write(valcode.content)
#     # 关闭文件流对象
#     f.close()
#     image = './valcode.jpg'
    tessdata_dir_config = '--tessdata-dir "D:\\tesseract-ocr\\tessdata"'
    pytesseract.pytesseract.tesseract_cmd = 'D:\\tesseract-ocr\\tesseract.exe'
    cap_code= pytesseract.image_to_string(Image.open(captua_url),config=tessdata_dir_config)
    return cap_code
#     image=image.convert('L') 
#     image.show()
#     threshold =127 
#     table = [] 
#     for n in range(256): 
#         if n < threshold: 
#             table.append(0) 
#         else: 
#             table.append(1)
#         image = image.point(table , '1') 
#         result = tesserocr.image_to_text(image) 
random_id,captua_url = get_randomId()
captua_url='https://www.newone.com.cn/'+str(captua_url)
captua_code1=captua_code(captua_url)
print(captua_code1.strip())
logging.captureWarnings(True)
print ("_xsrf的值是：" + random_id)
data = {"randomID":str(random_id),"actionName":"login_jiaoyi","url":"","username":"1808494215","password":"681218","code":captua_code1}
html=login(data)
soup=BeautifulSoup(html,"lxml",from_encoding='utf-8')
print(soup)


