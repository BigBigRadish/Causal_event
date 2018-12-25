# -*- coding: utf-8 -*-
'''
Created on 2018年12月25日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd
sina_jg_word1=pd.DataFrame()
sina_jg_word=pd.read_csv('sina_jg_word.csv')
file_1_2=sina_jg_word.sort_values(by="frequence" , ascending=False)
# print(file_1_2)
words=[]
frequence=[]
for index, i in file_1_2.iterrows():
    if len(str(i['word']))>=2  :
        words.append(str(i['word']))
        frequence.append(i['frequence'])
sina_jg_word1['word']=words
sina_jg_word1['frequence']=frequence      
print(sina_jg_word1)
sina_jg_word1.to_csv('./sina_jg_word1.csv') 
    