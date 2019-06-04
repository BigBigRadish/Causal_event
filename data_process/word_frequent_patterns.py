# -*- coding: utf-8 -*-
'''
Created on 2019年6月4日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#词语频繁模式挖掘 根据词性
import os
import codecs
import re
import pandas as pd
import sentence_parser
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

#基于词频的频繁模式挖掘
class treeNode:
    def __init__(self, name_value, num_occur, parent_node):
        self.name = name_value  # 节点元素名称
        self.count = num_occur  # 出现的次数
        self.node_link = None  # 指向下一个相似节点的指针，默认为None
        self.parent = parent_node  # 指向父节点的指针
        self.children = {}  # 指向孩子节点的字典 子节点的元素名称为键，指向子节点的指针为值

    def increase(self, num_occur):
        """
        增加节点的出现次数
        :param num_occur: 增加数量
        :return:
        """
        self.count += num_occur

    def disp(self, ind=1):
        print ('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)

if __name__ == '__main__':
    files_path='E:/Causal_events/forum50_articles_newline/'
    files=os.listdir(files_path)
    for file in files:
        with codecs.open(files_path+file,'r',encoding='utf-8') as f:
            lines = [line.strip() for line in f]
        print(lines)
        words = list(segmentor.segment(lines[0]))
        postags = list(postagger.postag(words))
        for word,postag in zip(words,postags):
            print(word,postag)
        break