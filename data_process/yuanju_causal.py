# -*- coding: utf-8 -*-
#调整格式
'''
Created on 2019年1月3日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd
import codecs
yuanju_causal=pd.read_csv('./yuanju_casual.csv')
k=1
for index,i in yuanju_causal.iterrows():
    yuanju=i['原句']
    effect=i['effect']
    tag=i['tag']
    cause=i['cause']
    list1=str(k)+':{原句:'+yuanju+'\n'+'原因句:'+effect+'\n'+'标签:'+tag+'\n'+'结果句:'+cause+'\n}\n'
    with codecs.open('./yuanju_causal.txt',mode='a',encoding='utf-8') as f:
                f.write(list1)
    k+=1