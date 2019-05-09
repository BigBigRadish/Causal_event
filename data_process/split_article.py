# -*- coding: utf-8 -*-
'''
Created on 2019年5月8日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#对51人经济论坛进行分句
import os
import asyncio
import codecs
from pyltp import SentenceSplitter
article_path='E:/Causal_events/forum50_articles'
files=os.listdir(article_path)

@asyncio.coroutine
def read_and_write(i):
    sum_sentence_path='E:/Causal_events/forum50_articles_newline/'
    with codecs.open('E:/Causal_events/forum50_articles/'+i,'r',encoding='utf-8') as f:
        txt=f.read()
        sents = SentenceSplitter.split(txt)
        for j in sents:
            with codecs.open(sum_sentence_path+i,'a',encoding='utf-8') as f1:
                f1.write(j.strip()+'\n')    
loop = asyncio.get_event_loop()
tasks = [read_and_write(i) for i in files]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()            