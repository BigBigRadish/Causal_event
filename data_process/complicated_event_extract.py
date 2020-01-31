# -*- coding: utf-8 -*-
'''
Created on 2018年12月25日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import os

import pandas as pd
import re

from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
from pyltp import SentenceSplitter

LTP_DIR =r'D:\LTP\MODEL\ltp_data'  # ltp模型目录的路径
segmentor = Segmentor()
segmentor.load(os.path.join(LTP_DIR, "cws.model"))# 分词模型路径，模型名称为`cws.model`

postagger = Postagger()
postagger.load(os.path.join(LTP_DIR, "pos.model"))# 词性标注模型路径，模型名称为`pos.model`

parser = Parser()
parser.load(os.path.join(LTP_DIR, "parser.model"))# 依存句法分析模型路径，模型名称为`parser.model

recognizer = NamedEntityRecognizer()
recognizer.load(os.path.join(LTP_DIR, "ner.model"))# 命名实体识别模型路径，模型名称为`ner.model`

# labeller = SementicRoleLabeller()
# labeller.load(os.path.join(LTP_DIR, 'pisrl_win.model'))# 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。

def typeof(variate):#判断变量类型的函数
    type=None
    if isinstance(variate,int):
        type = "int"
    elif isinstance(variate,str):
        type = "str"
    elif isinstance(variate,float):
        type = "float"
    elif isinstance(variate,list):
        type = "list"
    elif isinstance(variate,tuple):
        type = "tuple"
    elif isinstance(variate,dict):
        type = "dict"
    elif isinstance(variate,set):
        type = "set"
    return type

def get_full_semantic_from_part(sentencepart):#如果是列表需要去噪
    if '[' in sentencepart:
        sentencepart=sentencepart.replace('[','').replace(']','').replace("'",'').replace('“','')
        sen_part_list=sentencepart.split(',')
        for i in sen_part_list:
            if len(i.strip())<=4 :
                sen_part_list.remove(i)
        sen_part_list_1=sen_part_list.copy()

        for i in sen_part_list_1:
            if len(sen_part_list)>=2:
                # print(sen_part_list.copy())
                sen_part_list_2=sen_part_list_1.copy()
                sen_part_list_2.remove(i)
                flag=0
                for j in sen_part_list_2:
                    if i.strip() in j and flag==0:
                        # print(i,j)
                        # print(sen_part_list)
                        sen_part_list.remove(i)
                        flag=1
        sen_part_list_3=sen_part_list.copy()
        for i in sen_part_list_3:
            words_i = list(segmentor.segment(i))
            postags_i= list(postagger.postag(words_i))
            if filter_last_pos_v(postags_i):
                sen_part_list.remove(i)
        # print(sen_part_list)
        return sen_part_list
    else:
        words_i = list(segmentor.segment(sentencepart))
        postags_i= list(postagger.postag(words_i))
        if filter_last_pos_v(postags_i):
               return  []   
        else:
            return [sentencepart]

def filter_last_pos_v(postags):#是否过滤
    flag=False
    if 'n' not in postags and 'v' not in postags and 's' not in postags and 't' not in postags :
        flag=True
    elif len(postags)<2:
        flag=True
    elif postags[-1]=='n' and postags[-2]=='p' :
        flag=True
    return flag

def extract_events_by_postags(sentences):
    casual_sent=get_full_semantic_from_part(sentences)
    len_casual_sent=len(casual_sent)
    casual_sjs=[]
    if len_casual_sent!=0:
        for i in casual_sent:
            words_ = list(segmentor.segment(i.strip()))
            postags_= list(postagger.postag(words_))
            casual_sj=''
            for words_i,postag_i in zip(words_,postags_):
                if postag_i not in ['c','e','g','h','o','wp','x','r']:
                    casual_sj+=words_i
                # else:
                #     print(words_i)
            casual_sjs.append(casual_sj)
    return casual_sjs


path = r'H:/因果抽取_1/Causal_event/data/all_split_sentences.csv'
 
article_causality_sentence=pd.read_csv(path).drop_duplicates(subset=['yuanyin_part','jieguo_part'])#去重
casual_sj_1v1=pd.DataFrame()
total_1v1_yuan_yin_svs=[]
total_1v1_jie_guo_svs=[]
tags=[]
for index,i in article_causality_sentence.iterrows():
    yuanyin_svos=[]
    svos=1
    # print(len([]))
   
    # yuan_yin_part=get_full_semantic_from_part(i['yuanyin_part'])
    # jieguo_part= get_full_semantic_from_part(i['jieguo_part'])
    # print(yuan_yin_part,jieguo_part)


    yuan_yin_sjs=extract_events_by_postags(i['yuanyin_part'])
    jie_guo_sjs=extract_events_by_postags(i['jieguo_part'])
    if len(yuan_yin_sjs)==1 and len(jie_guo_sjs)==1:
        # print(yuan_yin_sjs,jie_guo_sjs)
        tags.append(i['tags'])
        total_1v1_yuan_yin_svs.append(yuan_yin_sjs)
        total_1v1_jie_guo_svs.append(jie_guo_sjs)
casual_sj_1v1['原因事件']=total_1v1_yuan_yin_svs
casual_sj_1v1['结果事件']=total_1v1_jie_guo_svs
casual_sj_1v1['标签']=tags
# casual_sj_1v1.to_csv('H:/因果抽取_1/Causal_event/data/casual_sj_1v1.csv',encoding='utf8')

