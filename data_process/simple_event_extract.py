# -*- coding: utf-8 -*-
'''
Created on 2019年12月21日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#简单事件抽取，通过，句法成分抽取,句子结构
#基础模块

from sentence_parser import LtpParser
import re
import os
from pymongo import MongoClient
import codecs
import pandas as pd
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
from pyltp import SentenceSplitter
LTP_DIR ="C:/Users/Administrator/Desktop/lzk/LTP/MODEL/ltp_data/"  # ltp模型目录的路径
segmentor = Segmentor()
segmentor.load(os.path.join(LTP_DIR, "cws.model"))# 分词模型路径，模型名称为`cws.model`
postagger = Postagger()
postagger.load(os.path.join(LTP_DIR, "pos.model"))# 词性标注模型路径，模型名称为`pos.model`
class TripleExtractor:
    def __init__(self):
        self.parser = LtpParser()

    '''文章分句处理, 切分长句，冒号，分号，感叹号等做切分标识'''
    def split_sents(self, content):
        return [sentence for sentence in re.split(r'[？?！!。；,;：:\n\r]', content) if sentence]

    '''利用语义角色标注,直接获取主谓宾三元组,基于A0,A1,A2'''
    def ruler1(self, words, postags, roles_dict, role_index,arcs,child_dict_list):
        v = words[role_index]
        head = arcs[role_index][2]
        child_dict = child_dict_list[role_index]
        role_info = roles_dict[role_index]
        # print(head)
        if 'A0' in role_info.keys() and 'A1' in role_info.keys():
            # print(words)
            s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2]+1) if
                         postags[word_index][0] not in ['w', 'x'  ] and words[word_index]])
            o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2]+1) if
                         postags[word_index][0] not in ['w', 'x'] and words[word_index]])
            if s  and o:
                return '1', {'s':s,'v':v,'o':o,'svo':s+v+o,'format':'svo','role':'A0+A1'}
            else:
                return '0',{}
       
            
        elif 'A1' in role_info:
            o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2]+1) if
                         postags[word_index][0] not in ['w', 'x']])
            # print(o)
            if o and 'SBV' in child_dict:
                e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                if e1 not in o:
                    # print({'s':e1,'v':v,'o':o,'svo':e1+v+o,'format':'svo','role':'A1+S'})
                    return '1',{'s':e1,'v':v,'o':o,'svo':e1+v+o,'format':'svo','role':'A1+S'}
                else:
                    return '0',{}
            elif o:
                # print({'v':v,'o':o,'svo':v+o,'format':'vo','role':'A1'})
                return '2',{'v':v,'o':o,'svo':v+o,'format':'vo','role':'A1'}
            else:
                return '0',{}
        elif 'A0' in role_info:
            # print(v)
            s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2] + 1) if
                         postags[word_index][0] not in ['w', 'x']])
            if s and 'VOB' in child_dict:
                    e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                    if e2 not in s:
                        # print({'s':s,'v':v,'o':e2,'svo':s+v+e2,'format':'svo','role':'A0+V'})
                        return '1',{'s':s,'v':v,'o':e2,'svo':s+v+e2,'format':'svo','role':'A0+V'}
                    else:
                        return '0',{}
            elif s:
                # print({'s':s,'v':v,'svo':s+v,'format':'sv','role':'A0'})
                return '2',{'s':s,'v':v,'svo':s+v,'format':'sv','role':'A0'}
            else:
                return '0',{}
        else:
            return '0',{}

    '''三元组抽取主函数'''
    def ruler2(self, words, postags, child_dict_list, arcs, roles_dict):
        svos = []
        words1=[]
        for index in range(len(postags)):
            tmp = 1
            # 先借助语义角色标注的结果，进行三元组抽取
            if index in roles_dict:
                # print(words,words[index])
                flag, triple = self.ruler1(words, postags, roles_dict, index,arcs,child_dict_list)
                if flag == '1':
                    svos.append(triple)
                    tmp = 0
                elif flag=='2':
                    svos.append(triple)
                    tmp = 0
                elif tmp == 1 :
                    # 如果语义角色标记为空，则使用依存句法进行抽取
                    if postags[index]:
                        relation = arcs[index][0]
                        head = arcs[index][2]
                    # 抽取以谓词为中心的事实三元组
                        child_dict = child_dict_list[index]
                        # 主谓宾
                        if 'SBV' in child_dict and 'VOB' in child_dict:
                            r = words[index]
                            e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                            
                            svos.append({'s':e1,'v':r,'o':e2,'svo':e1+r+e2,'format':'svo','role':'SVO'})

                        # 定语后置，动宾关系
                        elif relation == 'ATT':
                            if 'VOB' in child_dict:
                                e1 = self.complete_e(words, postags, child_dict_list, head - 1)
                                r = words[index]
                                e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                                temp_string = r + e2
                                if temp_string == e1[:len(temp_string)]:
                                    e1 = e1[len(temp_string):]
                                if temp_string not in e1:
                                    
                                    svos.append({'s':e1,'v':r,'o':e2,'svo':e1+r+e2,'format':'svo','role':'VOB'})#)#[e1, r, e2]
                        # 含有介宾关系的主谓动补关系
                        elif 'SBV' in child_dict and 'CMP' in child_dict:
                            e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                            cmp_index = child_dict['CMP'][0]
                            r = words[index] + words[cmp_index]
                            if 'POB' in child_dict_list[cmp_index]:
                                e2 = self.complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
                                # print({'s':e1,'v':r,'o':e2,'svo':e1+r+e2,'format':'svo','role':'SBV'})
                                svos.append({'s':e1,'v':r,'o':e2,'svo':e1+r+e2,'format':'svo','role':'SBV'})#e1+r+e2)#[e1, r, e2]    
                else:
                    return svos                  
        return svos

    '''对找出的主语或者宾语进行扩展'''
    def complete_e(self, words, postags, child_dict_list, word_index):
        child_dict = child_dict_list[word_index]
        prefix = ''
        if 'ATT' in child_dict:
            for i in range(len(child_dict['ATT'])):
                prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])
        postfix = ''
        if postags[word_index] == 'v':
            if 'VOB' in child_dict:
                postfix += self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            if 'SBV' in child_dict:
                prefix = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

        return prefix +words[word_index] + postfix
    
    #句中因果提取svo->sv->vo,svo,vo,sv;多因多果
    # def event_filter(self,svos):
        #

    '''程序主控函数'''
    def triples_main(self, content):
        # sentences = self.split_sents(content.replace('[','').replace(']','').replace("'",'').replace(',','，'))
        sentences = content.replace('[','').replace(']','').replace("'",'').replace(',','，')

        # svos1 = []
        # print(sentences)
        # for sentence in sentences:
        print(sentences)
        words, postags, child_dict_list, roles_dict, arcs = self.parser.parser_main(sentences)
        svos = self.ruler2(words, postags, child_dict_list, arcs, roles_dict)
        print(svos)

        # with codecs.open('C:/Users/Administrator/Desktop/lzk/Causal_event/data/test_sj.txt','a',encoding='utf-8') as f1:
        #     f1.write(str(sentences)+' '+str(svos)+'\n')       
        return svos
if __name__ == '__main__':
    tripleEx=TripleExtractor()
    path = r'C:/Users/Administrator/Desktop/lzk/Causal_event/data/all_split_sentences.csv'
    
    article_causality_sentence=pd.read_csv(path).drop_duplicates(subset=['yuanyin_part','jieguo_part'])#去重
    casual_sj_1v1=pd.DataFrame()
    total_1v1_yuan_yin_svs=[]
    total_1v1_jie_guo_svs=[]
    tags=[]
    for index,i in article_causality_sentence.iterrows():
        yuanyin_svos=[]
        # print(i['yuanyin_part'])

        yuan_yin_sjs=tripleEx.triples_main(i['yuanyin_part'])
        jie_guo_sjs=tripleEx.triples_main(i['jieguo_part'])
        # print(yuan_yin_sjs,jie_guo_sjs)

