# -*- coding: utf-8 -*-
'''
Created on 2018年11月28日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import os
import pandas as pd
from pymongo import MongoClient
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
from pyltp import SentenceSplitter
LTP_DIR = 'D:\LTP\MODEL\ltp_data'  # ltp模型目录的路径
segmentor = Segmentor()
segmentor.load(os.path.join(LTP_DIR, "cws.model"))# 分词模型路径，模型名称为`cws.model`
postagger = Postagger()
postagger.load(os.path.join(LTP_DIR, "pos.model"))# 词性标注模型路径，模型名称为`pos.model`
recognizer = NamedEntityRecognizer()
recognizer.load(os.path.join(LTP_DIR, "ner.model"))# 命名实体识别模型路径，模型名称为`ner.model`
parser = Parser()
parser.load(os.path.join(LTP_DIR, "parser.model"))# 依存句法分析模型路径，模型名称为`parser.model
if __name__ == '__main__':
    mongo_con=MongoClient('172.20.66.56', 27017)
    db=mongo_con.Causal_event
    collection=db.ner_extraction
    #extractor = CausalitySentencesExractor()
    path = r'E:\\Causal_events\\sina_articles_causality_extract'
    #sentence="我爱你,中国"
    files = os.listdir(path)
#     i=1251
    for file in files:
#         i+=1
#         while(file=='税务文明的核心是依法治税(2002.10.25).txt.csv'):
#             print(i)
        pathname = os.path.join(path, file)
        print(file)
        #准确获取一个txt的位置，利用字符串的拼接
        txt_path = pathname
        f = open(txt_path,'r',encoding='utf-8')
        article_causality_sentence=pd.read_csv(f).drop_duplicates(subset=['原因','结果'])
        #print(datas)
        yuanyin=[]
        jieguo=[]
        for index,i in article_causality_sentence.iterrows():
            words1 = segmentor.segment(i['原因'])#分词
            postags1 = postagger.postag(words1)#词性
            yuanyin_ners = recognizer.recognize(words1,postags1)#原因命名实体
            yuanyin=[]
            for index in range(0,len(postags1)):
                if postags1[index] in ['d','a']:
                    yuanyin.append(words1[index])
            print(yuanyin)
#             arcs = parser.parse(words1, postags1)  # 句法分析
#             i=0
#             s=''
#             for arc in arcs:
#                 print(arc.relation)
#                 if arc.relation in ['HED','SBV','VOB','COO','POB']:
#                     s+=words1[i]
#                 i+=1    
#             print(s)    
#             tag=i['标签']#事件标签
#             words2 = segmentor.segment(i['结果'])
#             print(list(words2))
#             postags2 = postagger.postag(words2)#词性
#             #jieguo_ners = recognizer.recognize(words2,postags2)#结果命名实体  
#             print(list(postags2))
            #yuanyin.append(','.join(yuanyin_ners))
            #jieguo.append(','.join(jieguo_ners))             
            #collection.insert({'栏目':'sina经济评论','文件名':i['文件名'],'原因实体':yuanyin,'结果实体':jieguo_ners,'标签':tag})
        #article_causality_sentence['原因命名实体']=yuanyin
        #article_causality_sentence['结果命名实体']=jieguo
        #article_causality_sentence.to_csv('E:\\Causal_events\\sina_economics_ner_extraction\\'+str(file))