# -*- coding: utf-8 -*-
'''
Created on 2019年4月7日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#文件批量重命名
import os
path='C:/Users/HP/git/Causal_event/pdf_data/raw_data/macro_research/'     
path1='C:/Users/HP/git/Causal_event/pdf_data/copy_of_data/macro_research'
#获取该目录下所有文件，存入列表中
f=os.listdir(path)

n=0
for i in f:
    print(i)
    #设置旧文件名（就是路径+文件名）
    oldname=path+f[n]
    
    #设置新文件名
    newname=path+str(n)+'.pdf'
    
    #用os模块中的rename方法对文件改名
    os.rename(oldname,newname)
    print(oldname,'======>',newname)
    n+=1