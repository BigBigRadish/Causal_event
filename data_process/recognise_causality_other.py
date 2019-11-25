# -*- coding: utf-8 -*-
'''
Created on 2018年11月17日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import re
import os
import codecs
import threading
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
from pyltp import SentenceSplitter
LTP_DIR = 'D:\LTP\MODEL\ltp_data'  # ltp模型目录的路径
segmentor = Segmentor()
segmentor.load(os.path.join(LTP_DIR, "cws.model"))# 分词模型路径，模型名称为`cws.model`
postagger = Postagger()
postagger.load(os.path.join(LTP_DIR, "pos.model"))# 词性标注模型路径，模型名称为`pos.model`
import pandas as pd
class CausalityExractor():
    def __init__(self):
        pass

    '''1由果溯因配套式'''
    def ruler1(self, sentence): 
        '''
        conm2:〈[之]所以,因为〉、〈[之]所以,由于〉、 <[之]所以,缘于〉
        [之]所以,因，[之]所以,归因于、[之]所以,由于、[之]所以,鉴于、[之]所以,由、 [之]所以,出于、 [之]所以,是因为
        conm2_model:<Conj>{Effect},<Conj>{Cause}
        '''
        a=[[],0]
        datas = list()
        word_pairs =[['之?所以', '因为'], ['之?所以', '由于'], ['之?所以', '缘于']\
                     ,['之?所以', '因'],['之?所以', '鉴于'],['之?所以', '由'],\
                     ['之?所以', '出于'],['之?所以', '是因为'],['的目的', '是']]
        for word in word_pairs:
            pattern = re.compile(r'\s?(%s)/[p|c|n]+\s(.*)(%s)/[p|c|v]+\s(.*)' % (word[0], word[1]))#将句子中的词和词性进行了拼接
#             print(sentence)
            result1 = pattern.findall(sentence)
            data = dict()
            if result1:
                a=[word,1]
                break
        return a
            

    def ruler10(self, sentence): 
        '''
        conm2:['起','作用'], ['是','原因'],['是','目的']
        conm2_model:<Conj>{Effect},<Conj>{Cause}
        '''
        datas = list()
        word_pairs =[['起','作用'], ['是','原因'],['是','目的'],['是','结果'],['是','证明']]
        a=[[],0]
        for word in word_pairs:
            pattern = re.compile(r'(%s)/[v]+\s(.*)(%s)/[n|v]+\s(.*)' % (word[0],word[1]))#将句子中的词和词性进行了拼接
#             print(sentence)
            
            result = pattern.findall(sentence)
            if result:
#                 print(sentence)
                a=[word,1]
                break
        return a
    '''2由因到果配套式'''
    def ruler2(self,sentence):
        '''
        conm1_model:<Conj>{Cause}, <Conj>{Effect}
        '''
        with codecs.open('../data/由因到果配套式_1_34__277.txt','r',encoding='utf-8') as fr:
            total_pair=fr.read()
        pairs=[i.split('-') for i in total_pair.split(',')]
#         datas = list()
        word_pairs =pairs
        a=[[],0]
        for word in word_pairs:
            pattern = re.compile(r'\s?(%s)/[p|c]+\s(.*)(%s)/[p|c|d]+\s(.*)' % (word[0], word[1]))
#             print(pattern)
#             print(sentence)
            result1 = pattern.findall(sentence)
#             print(result)
#             data = dict()
            if result1:
                a=[word,1]
                break
        return a
    def ruler11(self,sentence):#动词-动词，副词-副词
        '''
        conm1_model:<Conj>{Cause}, <Conj>{Effect}
        '''
        v_df_02=pd.read_csv('../data/d_df_o2.csv')#动词二元匹配
        v_df_02_150=v_df_02[v_df_02['support']>=0.001]#支持度>0.003,大于180
        total_pair=v_df_02_150['words'].values
#         print(total_pair)
        pairs=[i.split('-') for i in total_pair]
#         datas = list()
        word_pairs =pairs
        a=[[],0]
        for word in word_pairs:
            pattern = re.compile(r'\s?(%s)/[d|v]+\s(.*)(%s)/[d|v]+\s(.*)' % (word[0], word[1]))
#             print(pattern)
#             print(sentence)
            result1 = pattern.findall(sentence)
#             print(result)
#             data = dict()
            if result1:
                a=[word,1]
                break
        return a
    def ruler12(self,sentence):#动词-动词-动词
        '''
        conm1_model:<Conj>{Cause}, <Conj>{Effect}
        '''
        v_df_03=pd.read_csv('../data/v_df_o3.csv')#动词三元匹配
#         v_df_03_150=v_df_02[v_df_02['support']>=0.001]#支持度>0.003,大于180
        total_pair=v_df_03['words'].values
#         print(total_pair)
        pairs=[i.split('-') for i in total_pair]
#         datas = list()
        word_pairs =pairs
        a=[[],0]
        for word in word_pairs:
            pattern = re.compile(r'\s?(%s)/[d|v]+\s(.*)(%s)/[d|v]+\s(.*)(%s)/[d|v]+\s(.*)' % (word[0], word[1],word[2]))
#             print(pattern)
#             print(sentence)
            result1 = pattern.findall(sentence)
#             print(result)
#             data = dict()
            if result1:
                a=[word,1]
                break
        return a
    '''3由因到果居中式明确'''
    def ruler3(self, sentence):
        '''
        cons2:于是、所以、故、致使、以致[于]、因此、以至[于]、从而、因而、是因为、正因如此、那么
        cons2_model:{Cause},<Conj...>{Effect}
        '''
#         print(sentence)
        pattern1 = re.compile(r'(.*)[,，]+.*(由此|那么|让|于是|所以|故|致使|以致于?|因此|以至于?|从而|因而|正因?如此|才能|如此一来)/[p|c|v]+\s(.*)')
        result1 = pattern1.findall(sentence)
        data = dict()
        if result1:
            return [result1[0][1],1]
        else:
            return [[],0]
        
    '''4由因到果居中式精确'''
    def ruler4(self, sentence):#删除‘引导’、‘引入’,'决定','作用','|指引'，|推进\s+
        '''
        '''
        casual_verb=''
        with codecs.open('../data/由因到果居中式精确_28_153.txt','r',encoding='utf-8') as fr:
            total_pair=fr.read()
        pairs=total_pair.split(',')    
        for i in pairs:
            casual_verb+=i+'|'
        casual_verb=casual_verb[0:-1]#去掉最后一个斜杠
        pattern = re.compile(r'.*[,|，](.*)('+casual_verb+')/[p|c|d|v]+\s(.*)')
        result = pattern.findall(sentence)
        data = dict() 
        
        if result:
            return [result[0][1],1]
        else:
            return [[],0]
    '''5由因到果前端式模糊'''
    def ruler5(self, sentence):#去掉'按照'
        '''
        prep:为了、依据、为、按照、因[为]、按、依赖、照、比、凭借、由于、一旦
        prep_model:<Prep...>{Cause},{Effect}
        '''
        pattern = re.compile(r'\s?(为了|依据|因为|因|按|依赖|凭借|由于|一旦)/[d|p|c|v]+\s(.*)[,，]+(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
                return [result[0][0],1]
        else:
                return [[],0]

    '''6由因到果居中式模糊'''
    def ruler6(self, sentence):
        '''
        adverb:以免、以便、为此、才
        adverb_model:{Cause},<Verb|Adverb...>{Effect}
        '''
        pattern = re.compile(r'(.*)(以免|以便|为此|才|原因于此)\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            return [result[0][1],1]
        else:
            return [[],0]

    '''7由因到果前端式精确'''
    def ruler7(self, sentence):#既然?
        '''
        cons1:既[然]、因[为]、如果、由于、只要
        cons1_model:<Conj...>{Cause},{Effect}
        '''
        pattern = re.compile(r'\s?(因|因为|如果|由于|只要|随着|但凡)/[p|c|d|v]+\s(.*)+(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            return [result[0][0],1]
        else:
            return [[],0]
    '''8由果溯因居中式模糊'''
    def ruler8(self, sentence):
        '''
        3
        verb2:根源于、取决、来源于、出于、取决于、缘于、在于、出自、起源于、来自、发源于、发自、源于、根源于、立足[于]
        verb2_model:{Effect}<Prep...>{Cause}
        '''

        pattern = re.compile(r'(.*)(确实|根源于|取决|来源于|出于|取决于|缘于|在于|出自|起源于|来自|发源于|发自|源于|根源于|立足|立足于|受制于)/[p|c|d|v]+\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            return [result[0][1],1]
        else:
            return [[],0]
    '''9由果溯因居端式精确'''
    def ruler9(self, sentence):
        '''
        cons3:因为、由于
        cons3_model:{Effect}<Conj...>{Cause}
        '''
        pattern = re.compile(r'(.*)是?\s(因为|由于)/[p|c]+\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            return [result[0][1],1]
        else:
            return [[],0]

    '''抽取主函数'''
    def recognise_causality(self, sentence):
        infos = list()
      #  print(sentence)
        if self.ruler1(sentence)[1]:
            infos.append(self.ruler1(sentence)[0])
        elif self.ruler2(sentence)[1]:
            infos.append(self.ruler2(sentence)[0])
        elif self.ruler3(sentence)[1]:
            infos.append(self.ruler3(sentence)[0])
        elif self.ruler4(sentence)[1]:
            infos.append(self.ruler4(sentence)[0])
        elif self.ruler5(sentence)[1]:
            infos.append(self.ruler5(sentence)[0])
        elif self.ruler6(sentence)[1]:
            infos.append(self.ruler6(sentence)[0])
        elif self.ruler7(sentence)[1]:
            infos.append(self.ruler7(sentence)[0])
        elif self.ruler8(sentence)[1]:
            infos.append(self.ruler8(sentence)[0])
        elif self.ruler9(sentence)[1]:
            infos.append(self.ruler9(sentence)[0])
        elif self.ruler10(sentence)[1]:
            infos.append(self.ruler10(sentence)[0])
        elif self.ruler11(sentence)[1]:
            infos.append(self.ruler11(sentence)[0])
        elif self.ruler12(sentence)[1]:
            infos.append(self.ruler12(sentence)[0])
        else:
            return[[],0]
        return [infos,1]

    '''抽取主控函数'''
    def extract_main(self, content):
        content=self.process_content(content)
        for sent in set(content):
            words=list(segmentor.segment(sent))
            postags = list(postagger.postag(words))
            sent1 = ' '.join([word + '/' + postag for word,postag in zip(words,postags)])
#             print(sent1)
            result = self.recognise_causality(sent1)
#             print(sent)
#             print(result)
#             print(result)
            if result[1]:
                mu = threading.Lock()
                with codecs.open('../data/test_sentences_ture.txt','a',encoding='utf-8') as f:
                    if  mu.acquire(True): #确保文件写入成功
                        f.write(sent.replace('\n','')+'  '+str(result[0]).replace('[','').replace(']','')+'\n')
                        f.flush()
                        os.fsync(f)
                        f.close()
                        mu.release()
#                 return (sent,result[0])
            else:
                with codecs.open('../data/test_sentences_false.txt','a',encoding='utf-8') as f2:
                    f2.write(sent+'\n') 
#         return datas

    '''文章分句处理'''
    def process_content(self, content):
        return [sentence for sentence in SentenceSplitter.split(content) if sentence]

    '''切分最小句'''
    def fined_sentence(self, sentence):
        return re.split(r'[？！；]', sentence)

if __name__ == '__main__':
    extractor = CausalityExractor()
#     path_= r'../data/other_sentences.txt'
#     with codecs.open(path_,'r',encoding='utf-8') as fr:
#         total_content=fr.read()
#     
#     extractor.extract_main(total_content)
    path_= r'../data/test_2.csv'
    with codecs.open(path_,'r',encoding='utf-8') as fr:
        total_content=fr.readlines()
    # for line in total_content:
    #     if(',1' in line):
    #         with codecs.open('../data/test_true.txt','a',encoding='utf-8') as fw:
    #             fw.write(line)
    #     else:
    #         with codecs.open('../data/test_false.txt','a',encoding='utf-8') as fw_1:
    #             fw_1.write(line)
            
            
     
    extractor.extract_main(''.join([line.split(',')[0] for line in total_content]))

