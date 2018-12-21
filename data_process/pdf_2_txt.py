# -*- coding: utf-8 -*-
'''
Created on 2018年12月21日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import os
import sys
type = sys.getfilesystemencoding()
from PyPDF2 import PdfFileReader, PdfFileWriter
readFile = r'C:\Users\HP\git\Causal_event\data_process\宏观研究\2012年10月份CPI、PPI数据快评-需求端改善有限.pdf'
fp = open(readFile,'rb')
pdfFile = PdfFileReader(fp)
if pdfFile.isEncrypted:
    try:
        pdfFile.decrypt('')
        print('File Decrypted (PyPDF2)')
    except:
        command = str("cp "+ readFile +
            " temp.pdf; qpdf --password='' --decrypt temp.pdf " + readFile+ "; rm temp.pdf")
        os.system(command)
        print('File Decrypted (qpdf)')
        fp = open(readFile.encode(type))
        pdfFile = pdfFile(fp)
else:
    print('File Not Encrypted')
#dostuff with pdfFile here
# 获取 PDF 文件的文档信息
documentInfo = pdfFile.getDocumentInfo()
print('documentInfo = %s' % documentInfo)
# 获取页面布局
pageLayout = pdfFile.getPageLayout()
print('pageLayout = %s ' % pageLayout)

# 获取页模式
pageMode = pdfFile.getPageMode()
print('pageMode = %s' % pageMode)

xmpMetadata = pdfFile.getXmpMetadata()
print('xmpMetadata  = %s ' % xmpMetadata)

# 获取 pdf 文件页数
pageCount = pdfFile.getNumPages()

print('pageCount = %s' % pageCount)
for index in range(0, pageCount):
    # 返回指定页编号的 pageObject
    pageObj = pdfFile.getPage(index)
    print('index = %d , pageObj = %s' % (index, type(pageObj)))  # <class 'PyPDF2.pdf.PageObject'>
    # 获取 pageObject 在 PDF 文档中处于的页码
    pageNumber = pdfFile.getPageNumber(pageObj)
    print('pageNumber = %s ' % pageNumber)
