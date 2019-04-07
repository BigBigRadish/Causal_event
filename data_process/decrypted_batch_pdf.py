# -*- coding: utf-8 -*-
'''
Created on 2019年4月7日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#批量破解pdf密码
import subprocess
import  os
path = r"C:/Users/HP/git/Causal_event/qpdf-8.4.0/bin"
pre = r"C:/Users/HP/git/Causal_event/pdf_data/raw_data/macro_research"  #初始pdf文件夹
final = r"C:/Users/HP/git/Causal_event/pdf_data/copy_of_data/macro_research"     #存放破解的pdf的文件夹
files = os.listdir(pre)
exit_files = os.listdir(final)
for j  in files:
    if j not in exit_files:
        abs_file = os.path.join(pre,j)
        out_file = os.path.join(final,j)
        cmd = ["qpdf","--decrypt",abs_file,out_file]  #命令行终端命令
        sub = subprocess.Popen(args=cmd,cwd=path,shell=True)  #不要忘记cwd
        sub.wait()   #最好加上，否则可能由于多个进程同时执行带来机器瘫痪
