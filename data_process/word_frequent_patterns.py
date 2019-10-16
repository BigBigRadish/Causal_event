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
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
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
def eclat(prefix, items, min_support, freq_items):
    while items:
        # 初始遍历单个的元素是否是频繁
        key, item = items.pop()
        key_support = len(item)
        if key_support >= min_support:
            # print frozenset(sorted(prefix+[key]))
            freq_items[frozenset(sorted(prefix+[key]))] = key_support
            suffix = []  # 存储当前长度的项集
            for other_key, other_item in items:
                new_item = item & other_item  # 求和其他集合求交集
                if len(new_item) >= min_support:
                    suffix.append((other_key, new_item))
            eclat(prefix+[key], sorted(suffix, key=lambda item: len(item[1]), reverse=True), min_support, freq_items)
    return freq_items


def eclat_zc(data_set, min_support=1):
    """
    Eclat方法
    :param data_set:
    :param min_support:
    :return:
    """
    # 将数据倒排
    data = {}
    trans_num = 0
    for trans in data_set:
        trans_num += 1
        for item in list(segmentor.segment(trans)):
            if item not in data:
                data[item] = set()
            data[item].add(trans_num)
    freq_items = {}
    freq_items = eclat([], sorted(data.items(), key=lambda item: len(item[1]), reverse=True), min_support, freq_items)
    return freq_items
def test_eclat(minSup, dataSetDict, dataSet):
    freqItems = eclat_zc(dataSet, minSup)
    freqItems = sorted(freqItems.items(), key=lambda item: item[1])
    return freqItems
def loadDblpData(inFile):#加载数据集
    '''
        加载数据
    :param inFile:
    :return:
    '''
    with codecs.open(files_path+inFile,'r',encoding='utf-8') as f:
        lines = [line.strip() for line in f]
        print(lines)
#         words = list(segmentor.segment(lines[0]))
    dataSetDict = {}
    dataSet = []
    for line in lines:
        dataSet.append(line)
        print(line)
        dataLine = list(segmentor.segment(line))
        print(dataLine)
        dataSetDict[frozenset(dataLine)] = dataSetDict.get(frozenset(dataLine), 0) + 1
    return dataSetDict, dataSet
if __name__ == '__main__':
#     files_path='E:/Causal_events/forum50_articles_newline/'
#     files=os.listdir(files_path)
# #     for file in files:
#     dataSetDict, dataSet=loadDblpData(files[0])
#     freqItems=test_eclat(3, dataSetDict, dataSet)
#     print(freqItems)
#     postags = list(postagger.postag(words))
#     for word,postag in zip(words,postags):
#         print([word,postag])
#     break
    big_l=[]
    n_df=pd.read_csv('../data/ad_df.csv')
#     print(n_df.words)
#     n_dummy_df=n_df.str.get_dummies(',')
#     print(n_dummy_df.head(5))
    n_df_v=n_df.dropna().words.values
    for i in n_df_v:
        if i!='':
            print(i)
            big_l.append(i.split(','))
    Encoder=TransactionEncoder()
    encoder_data=Encoder.fit_transform(big_l)
    df=pd.DataFrame(encoder_data,columns=Encoder.columns_)
    print(df.head(5))
    frequent_items=apriori(df, min_support=0.001, use_colnames=True, max_len=3).sort_values(by='support',ascending=False)
    frequent_items.to_csv('../data/ad_df_fq_001.csv')
    