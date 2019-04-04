# -*- coding: utf-8 -*-
'''
Created on 2018年12月21日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os
import pikepdf

def convert_pdf_to_txt(path,save_name):#读取成txt格式
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    try:
        with open("%s"%save_name,"w") as f:#格式化字符串还能这么用！
            for i in str:
                f.write(i)
        print ("%s Writing Succeed!"%save_name)
    except:
        print ("Writing Failed!")


               
if __name__ == '__main__': 
    raw_file_dirs=['行业研究','宏观研究','策略研究','公司研究']
    for i in raw_file_dirs:
        rootdir = 'C:/Users/HP/git/Causal_event/pdf_data/raw_data/'+i
        files = os.listdir(rootdir) #列出文件夹下所有的目录与文件
        for i in range(0,len(list)):
            path = os.path.join(rootdir,files[i])
            if os.path.isfile(path):
                pdf = pikepdf.open(path)#奖pdf重新存储，可以读取
                pdf.save('C:/Users/HP/git/Causal_event/pdf_data/copy_of_data/'+i+'/'+files[i])#重新存储解密 
#     url = r"./macro_Research/2012年10月份CPI、PPI数据快评-需求端改善有限1.pdf"
                convert_pdf_to_txt(path,('C:/Users/HP/git/Causal_event/pdf_data/copy_of_data/'+i+'/'+files[i]).replace('pdf','txt'))#转换成txt文件


