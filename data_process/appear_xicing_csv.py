# -*- coding: utf-8 -*-
'''
Created on 2019年10月15日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#根据词性，挑选句子对
import os
import codecs
import re
import pandas as pd
import sentence_parser
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
def postag_list(file,n_postags,line_total):
    with codecs.open(file,'r',encoding='utf-8') as f:
            lines = [line.split(' ')[0].strip() for line in f]
    for line in lines:
        with codecs.open('../data/causality_sentences_2.txt','a',encoding='utf-8') as fw:
            fw.write(line+'\n')
        sus_pos_wors=[]
        words=list(segmentor.segment(line))
        postags = list(postagger.postag(words))
        for word,postag in zip(words,postags):
            if postag in n_postags and len(word)>=2:
                sus_pos_wors.append(word)
        line_total.append(','.join(sus_pos_wors))
    return line_total
if __name__ == '__main__':
    file_path='../data/causality_sentences.txt'
    n_postags=['j','n','nd','nh','ni','ns','nt','nz','ws','nl']#名词
    v_postags=['v']#动词
    d_postags=['d']#副词
    ad_postags=['d','a','b']
    line_total=[]
    total_line=postag_list(file_path,n_postags,line_total)
#     print(total_line)
    n_df=pd.DataFrame(total_line)
    n_df.to_csv('../data/n_df.csv',encoding='utf-8')

            
                    
        