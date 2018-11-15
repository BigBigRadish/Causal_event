# -*- coding: utf-8 -*-
'''
Created on 2018年11月13日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import selenium
from PIL import Image,ImageEnhance
from selenium import  webdriver
import pytesser3
import pytesseract
import time
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
    authCodeText = pytesseract.image_to_string(authcodeImg,config=tessdata_dir_config).strip()
    print(authCodeText)
    return authCodeText

def newone_login(driver,account,passwd,authCode):
    '''登录招商证券系统'''
    driver.find_element_by_id('username').send_keys(account)#用户名
    driver.find_element_by_id('password').send_keys(passwd)#密码
    driver.find_element_by_id('code').send_keys(authCode)#验证码
    driver.find_element_by_id('loginBtn').click()
    time.sleep(2)
def crawl_articles_detail(driver):
    driver.get('http://www.newone.com.cn/researchcontroller/search')
    driver.find_eleme_by_id('page')['value']="2"
    driver.find_eleme_by_id('page')['value']
    

if __name__ == '__main__':

    driver = webdriver.Chrome()
    driver.get('https://www.newone.com.cn/nwsecure/login_jiaoyi')#打开登陆网站
    driver.maximize_window()
    imgElement = driver.find_element_by_id('codeimg')#获取图片元素
    authCodeText = get_auth_code(driver,imgElement)
    newone_login(driver,'1808494215','681218',authCodeText)
    #print(driver.get_cookies())#获取到cookies了
    #driver.get('http://www.newone.com.cn/researchcontroller/detail?id=227696')
#     driver.quit()


