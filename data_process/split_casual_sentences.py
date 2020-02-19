# -*- coding: utf-8 -*-
'''
Created on 2019年12月18日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#因果句分裂成两部分，超参数Rest_min_max_len=4
import codecs
import os
import re
import pandas as pd
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
from pyltp import SentenceSplitter

LTP_DIR = 'D:\LTP\MODEL\ltp_data'  # ltp模型目录的路径
segmentor = Segmentor()
segmentor.load(os.path.join(LTP_DIR, "cws.model"))# 分词模型路径，模型名称为`cws.model`
postagger = Postagger()
postagger.load(os.path.join(LTP_DIR, "pos.model"))# 词性标注模型路径，模型名称为`pos.model`

Rest_min_max_len=4#超参数Rest_min_max_len=4

single_words_set_guideyuanyin= ['若','假定','只要','若是','倘或','论及','倘若','万一',\
                    '倘然','若果','设使','如其','如若','假如','设或','设若',\
                '要是','因为','因','按','凭借','由于','一旦','一经','依据',\
                 '如果','随着','立足于','受制','通过','借助','直到','只有',\
                '但凡','根源于','取决','来源于','出于','取决于','缘于','在于',\
                '出自','起源于','来自','发源于','发自','源于']#引导原因集合

single_words_set_guidejieguo=['由此','那么','让','于是','所以','故','致使','以致','以致于','因此','以至',\
                '以至于','从而','因而','正如此','正因如此','才能','如此一来','进一步','出于',\
                '确保','实现','招致','踏入','循循诱人','启迪','触发','敦促','步入',\
                '引起','切入','带来','有助于','涉及','引致','引诱','兼及','启发','推进',\
                '推涛作浪','乘虚而入','驱动','牵动','唤起','拥入','掀起','导向','排入','引向',\
                '涌入','破门而入','勾引','沁入','事关','飞进','跃入','渗入','映入','使','波及',\
                '诱发','拉动','倘然','引来','驱使','推动','促进','利诱','挑动','因势利导','推波助澜',\
                '威胁利诱','跨入','滋生','以致','挑起','推向','促成','促使','引发','诱使','关涉','造成',\
                '关乎','煽惑','引蛇出洞','促进','设使','触及','涉嫌','归于','导致','后浪推前浪','关系',\
                '诱致','做成','一拥而入','使得','酿成','致使','带动','力促','诱导','闯进','调进','诱惑',\
                '遁入','助长','引导','导引','旁及','吸引','引出','接触','百川归海','指引','引入','招引',\
                '责有攸归','有利于','才能','为了','以免','以便','为此','才','确实','吸引','面临','拉动',\
                '刺激','变成','下行','促使','激发','加剧','步入','抑制','着力','指引','推动','推进','有望',\
                '放缓','迫使','推向','放宽，期待','操纵','加快','显现','鼓励','提振','助长','遭到','凸显',\
                '拓宽','蔓延','滋生','塑造','整顿','误导','旨在','强化','已经','越来越','不断','逐步','尤其',\
                '最终','就要','依然','几乎','日益','稳步','一度','随后','结果','以便','相继','那么','日趋',\
                '终究','更加','随之','不能不','不得不','不至于','即将','势必','只有','更为','实际上','尽可能']
with codecs.open(r'E:/因果抽取_1/Causal_event/data/由果溯因所有词组.txt',encoding='utf-8') as f1:
    gy_words=f1.read().split(',')


with codecs.open(r'E:/因果抽取_1/Causal_event/data/由因溯果所有词组.txt',encoding='utf-8') as f1:
    yg_words=f1.read().split(',')


triple_words=pd.read_csv(r'E:/因果抽取_1/Causal_event/data/v_df_o3.csv',encoding='utf-8')
triple_guide_words=triple_words[:88].words.values#超参数，取多大的置信度，三元tag触发词典



def get_subsents(sentences):#得到子句
    if '，' in sentences:
        subsents=sentences.split('，')
    else:
        subsents=[sentences]
    return subsents

def judeg_subsents_len(subset,subse):#判断其他子句是否有小于指定长度的句子
    len_flag=False
    subs=subset.copy()#需要拷贝，不然会引用
    # print(subs)
    subs.remove(subse)
    # print(subs)
    for i in subs:
        if len(i)<5:#超参
            len_flag=True
            break
    return len_flag
               
def filter_casual_sentences(sentences,words):#过滤tag所在子句带？号，或者单句带？；words表示tag组
    sentences=sentences.replace(',','，').replace('?','？').replace('!','。').replace('.','。')#预处理
    subsents=get_subsents(sentences)
    subsents_len=len(subsents)
    filter_tag=False
    if '，' not in sentences and '？' in sentences:
        filter_tag=True
    elif '，'  in sentences and '？' in sentences:
        for word in words:
            for i in range(subsents_len):
                if word in subsents[i] and '？' in  subsents[i]:
                    filter_tag=True
                    break
    elif len(words)==1 and subsents_len==1:#某些因果引导词在句首
        word_len=len(words[0])
        if sentences[:word_len-1]==words[0] and words[0] in []:#某些必须两句以上使用的词？
            filter_tag=True
    # print(filter_tag)
        
    return filter_tag#是否过滤该条语句

def judge_tag_position_in_sentences_1(sentences,word):#一元tag,判断在句子中的位置，以及tag所在子句的位置
    tag_len=len(word)#tag的长度
    tag_head=False
    if '，' in sentences:
        sentens_pos=0
        subsents= get_subsents(sentences)#得到子句列表
        subsents_len=len(subsents)
        for i in range(subsents_len):
            if word in subsents[i]:
                sentens_pos=i
    else:
        sentens_pos=0
        subsents=[sentences]
    if subsents[sentens_pos][:tag_len]==word:
            tag_head=True
    return subsents,sentens_pos,tag_head#返回，子句组，所在子句的位置，以及是否在头部

def judge_tag_position_in_sentences_2(sentences,words):#二元tag,判断在句子中的位置，以及tag所在子句的位置
    tag1=words[0]
    tag2=words[1]
    subsents,tag1_sentens_pos,tag1_head=judge_tag_position_in_sentences_1(sentences,tag1)
    _,tag2_sentens_pos,tag2_head=judge_tag_position_in_sentences_1(sentences,tag2)
    return subsents,tag1_sentens_pos,tag2_sentens_pos,tag1_head,tag2_head#返回子句集合，所在子句的位置，以及tag的位置

def judge_tag_position_in_sentences_3(sentences,words):#三元tag,判断在句子中的位置，以及tag所在子句的位置
    tag1=words[0]
    tag2=words[1]
    tag3=words[2]
    subsents,tag1_sentens_pos,tag1_head=judge_tag_position_in_sentences_1(sentences,tag1)
    _,tag2_sentens_pos,tag2_head=judge_tag_position_in_sentences_1(sentences,tag2)
    _,tag3_sentens_pos,tag3_head=judge_tag_position_in_sentences_1(sentences,tag3)
    return subsents,tag1_sentens_pos,tag2_sentens_pos,tag3_sentens_pos,tag1_head,tag2_head,tag3_head#返回子句集合，所在子句的位置，以及各个tag的位置

def get_posion_in_subsent(sentence,tag):#获取词在子句中的位置
    # print(sentence)
    current_position=len(sentence.split(tag)[0])-1#词的开始位置
    rest_len=len(sentence.split(tag)[1])#剩余句子长度
    return current_position,rest_len

def get_p_in_subsent(sentence,tag):#得到右半段连词的位置
    # print(sentence)
    right_sents=sentence.split(tag)[1]#因果词在右半边
    left_len=len(sentence.split(tag)[0])
    p_flag=False
    p_right_index=0
    p_word=''
    words=list(segmentor.segment(right_sents))
    postags = list(postagger.postag(words))
    # print(words)
    # print(postags)
    p_noise_words=['和','但','却','或','与','不仅','或是','或者','并','且','及','以及','并且','如果','虽然']#连词过滤
    if 'c' in postags:
        p_right_index=postags.index('c')
        p_flag=True
        p_word=words[p_right_index]
        if p_word in p_noise_words:
            p_word=''
            p_flag=False
    else:
        pass
    return p_flag,p_word

def middle_tags_rule(subsents,words):#引导词在子句中间分裂规则?
    yuanyin_sents=''
    jieguo_sents=''
    p_word_1=''
    if len(words)==1:
        single_sentence=subsents[0]
        tag=words[0]
        p_flag,p_word_1=get_p_in_subsent(single_sentence,tag)
        causal_data_array=single_sentence.split(tag)#部分居中倒装需要判断,部分需要丢弃
        if p_flag and tag in single_words_set_guideyuanyin and p_word_1!='':#先判断是否存在连词
                pattern = re.compile(r'(.*)(%s)(.*)(%s)(.*)' % (tag, p_word_1))
                result1 = list(pattern.findall(single_sentence))
                # print(result1)
                lef_sents_len=len(result1[0][2])
                right_sents_len=len(result1[0][4])
                if lef_sents_len>=Rest_min_max_len and right_sents_len>=Rest_min_max_len:#超参数
                    yuanyin_sents=result1[0][2]
                    jieguo_sents=result1[0][4]


        elif tag in ['假定','只要','若是','倘或','论及','倘若','万一','只有',\
                    '倘然','若果','设使','如其','如若','假如','设或','设若',\
                '要是','因为','按','由于','一旦','一经','依据','但凡''如果','随着','直到','如其']:
            yuanyin_sents=causal_data_array[1]
            jieguo_sents=causal_data_array[0]
        elif tag in ['根源于','取决','来源于','出于','取决于','缘于','在于',\
                '出自','起源于','来自','发源于','发自','源于','凭借','借助','立足于','受制']:
            yuanyin_sents=tag+causal_data_array[1]
            jieguo_sents=causal_data_array[0]
        elif tag in ['由此','那么','让','于是','所以','故','致使','以致','以致于','因此','以至',\
                '以至于','从而','因而','正如此','正因如此','如此一来','进一步','出于','使',\
                '以致','归于','为了','以免','以便','为此','才','有望','旨在','已经','越来越','不断','逐步','尤其',\
                '最终','就要','依然','几乎','日益','稳步','一度','随后','结果','以便','相继','那么','日趋',\
                '终究','更加','随之','不能不','不得不','不至于','即将','势必','只有','更为','实际上','尽可能']:#引导结果（不加tag）
            yuanyin_sents=causal_data_array[0]
            jieguo_sents=causal_data_array[1] 
        elif tag in [
                '才能','确保','实现','招致','踏入','投入','循循诱人','启迪','触发','敦促','步入',\
                '引起','切入','带来','有助于','涉及','引致','引诱','兼及','启发','推进',\
                '推涛作浪','乘虚而入','驱动','牵动','唤起','拥入','掀起','导向','排入','引向',\
                '涌入','破门而入','勾引','沁入','事关','飞进','跃入','渗入','映入','波及',\
                '诱发','拉动','倘然','引来','驱使','推动','促进','利诱','挑动','因势利导','推波助澜',\
                '威胁利诱','跨入','滋生','挑起','推向','促成','促使','引发','诱使','关涉','造成',\
                '关乎','煽惑','引蛇出洞','促进','设使','触及','涉嫌','导致','后浪推前浪','关系',\
                '诱致','做成','一拥而入','使得','酿成','致使','带动','力促','诱导','闯进','调进','诱惑',\
                '遁入','助长','引导','导引','旁及','吸引','引出','接触','百川归海','指引','引入','招引',\
                '责有攸归','有利于','才能','确实','吸引','面临','拉动','刺激','变成','下行','促使','激发',\
                '加剧','步入','抑制','着力','指引','推动','推进','放缓','迫使','推向','放宽，期待','操纵',\
                '加快','显现','鼓励','提振','助长','遭到','凸显','拓宽','蔓延','滋生','塑造','整顿','误导','强化']:#引导结果（加tag）
            # print(tag)
            yuanyin_sents=causal_data_array[0]
            jieguo_sents=tag+causal_data_array[1]
    if len(yuanyin_sents.strip())<Rest_min_max_len or len(jieguo_sents.strip())<Rest_min_max_len:#设置子句最短长度，超参数
        yuanyin_sents=''
        jieguo_sents=''
    # print(yuanyin_sents,jieguo_sents)
    return yuanyin_sents,jieguo_sents,p_word_1

def first_tags_rule(subsents,words):#引导词在子句前端分裂规则?
    pass

def backend_tags_rule(subsents,words):#引导词在子句后端分裂规则?
    pass

def split_sentences(sentences,words):#分裂句子，分裂后的原因部分和结果部分分别完整保留
    yuanyin_sents=''
    jieguo_sents=''
    tags=words
    if filter_casual_sentences(sentences,words):
        return yuanyin_sents,jieguo_sents
    
    if len(words)==1:
        tag=words[0]
        tags=tag
        # print(tag)
        subsents,sentens_pos,tag_head=judge_tag_position_in_sentences_1(sentences,tag)
        # print(subsents)
        subsents_len=len(subsents)#子集长度
        # print(tag_head)
        if subsents_len!=1 and tag_head:#这种情况最多
            if tag in single_words_set_guideyuanyin:#单个词引导原因

                if tag in subsents and sentens_pos>0:#如果作为中间独有的分隔符
                    yuanyin_sents=subsents[sentens_pos+1:]
                    jieguo_sents=subsents[:sentens_pos]
                elif tag in subsents and sentens_pos==0:#tag，,直接去掉（去噪）
                    yuanyin_sents=''
                    jieguo_sents=''
                elif sentens_pos==0:#子句位置在句首
                    yuanyin_sents=subsents[0]
                    jieguo_sents=subsents[1:]
                elif sentens_pos==subsents_len-1:#子句位置在句尾
                    yuanyin_sents=subsents[sentens_pos]
                    jieguo_sents=subsents[:sentens_pos]
                else:
                    yuanyin_sents=subsents[sentens_pos]
                    jieguo_sents=subsents[sentens_pos+1:]

            elif tag in single_words_set_guidejieguo:#单个词引导结果

                if tag in subsents and sentens_pos>0:#如果作为中间独有的分隔符
                    yuanyin_sents=subsents[sentens_pos+1:]
                    jieguo_sents=subsents[:sentens_pos]
                elif tag in subsents and sentens_pos==0:#tag，,直接去掉（去噪）
                    yuanyin_sents=''
                    jieguo_sents=''
                elif sentens_pos==0:
                    jieguo_sents=subsents[0]
                    yuanyin_sents=subsents[1:]
                else:
                    jieguo_sents=subsents[sentens_pos]
                    yuanyin_sents=subsents[:sentens_pos]
            else:
                yuanyin_sents=''
                jieguo_sents=''
        elif subsents_len==1 and tag_head!=True:
            #引导词在子句中间分裂规则
                # print(100)
                # print(tag)
                yuanyin_sents,jieguo_sents,p_word=middle_tags_rule(subsents,[tag])
                if yuanyin_sents!='' and jieguo_sents!='' and p_word!='':
                    tags=tags+'-'+p_word
                    # print(tags)
        elif subsents_len==1 and  tag_head:
            # if tag in []:#引导词在子句前端分裂规则
            #     first_tags_rule(subsents,[tag])
            yuanyin_sents=''
            jieguo_sents=''
        else:
            if tag in single_words_set_guideyuanyin:#单个词引导原因，子句集长度>1,tag所在位置不在开头或末尾
                # print(subsents,tag)
                # print(sentens_pos)

                len_target=len(subsents[sentens_pos])
                current_position,rest_len=get_posion_in_subsent(subsents[sentens_pos],tag)#//得到所在词当前的位置
                p_flag,p_word=get_p_in_subsent(subsents[sentens_pos],tag)

                if p_flag and tag in ['因为','因']:#这两个最明显
                    pattern = re.compile(r'(.*)(%s)(.*)(%s)(.*)' % (tag, p_word))
                    result1 = list(pattern.findall(subsents[sentens_pos]))
                    # print(result1)
                    lef_sents_len=len(result1[0][2])
                    right_sents_len=len(result1[0][4])
                    if lef_sents_len>=Rest_min_max_len and right_sents_len>=Rest_min_max_len:
                        yuanyin_sents=result1[0][2]
                        jieguo_sents=result1[0][4]
                        tags=tags+'-'+p_word
                        # print(yuanyin_sents,jieguo_sents,tags)
                    elif 0<sentens_pos and sentens_pos<len(subsents)-1:
                        yuanyin_sents=subsents[sentens_pos]
                        jieguo_sents=subsents[sentens_pos+1:]
                    elif sentens_pos==len(subsents)-1:
                        yuanyin_sents=subsents[sentens_pos]
                        jieguo_sents=subsents[:sentens_pos]
                        # print(sentences)
                    else:
                        pass
                        
                
                elif current_position<5 and rest_len>=Rest_min_max_len and sentens_pos!=subsents_len-1:#超参数
                    yuanyin_sents=subsents[sentens_pos]
                    jieguo_sents=subsents[sentens_pos+1:]
                    # print(yuanyin_sents,jieguo_sents)
                elif current_position>=5 and rest_len>=Rest_min_max_len and sentens_pos==subsents_len-1:#超参数
                    yuanyin_sents=subsents[sentens_pos]
                    jieguo_sents=subsents[:sentens_pos]
                    
                else:
                    yuanyin_sents,jieguo_sents,p_word=middle_tags_rule([subsents[sentens_pos]],[tag])
                    tags=tags+'-'+p_word
                    # print(yuanyin_sents,jieguo_sents,tag)
        

            elif tag in single_words_set_guidejieguo:#单个词引导结果
                '''
                ['由此','那么','让','于是','所以','故','致使','以致','以致于','因此','以至',\
                '以至于','从而','因而','正如此','正因如此','才能','如此一来','进一步','出于',\
                '确保','实现','招致','踏入','循循诱人','启迪','触发','敦促','步入','如何'\
                '引起','切入','带来','有助于','涉及','引致','引诱','兼及','启发','推进',\
                '推涛作浪','乘虚而入','驱动','牵动','唤起','拥入','掀起','导向','排入','引向',\
                '涌入','破门而入','勾引','沁入','事关','飞进','跃入','渗入','映入','使','波及',\
                '诱发','拉动','倘然','引来','驱使','推动','促进','利诱','挑动','因势利导','推波助澜',\
                '威胁利诱','跨入','滋生','以致','挑起','推向','促成','促使','引发','诱使','关涉','造成',\
                '关乎','煽惑','引蛇出洞','促进','设使','触及','涉嫌','归于','导致','后浪推前浪','关系',\
                '诱致','做成','一拥而入','使得','酿成','致使','带动','力促','诱导','闯进','调进','诱惑',\
                '遁入','助长','引导','导引','旁及','吸引','引出','接触','百川归海','指引','引入','招引',\
                '责有攸归','有利于','才能','为了','以免','以便','为此','才','确实','吸引','面临','拉动',\
                '刺激','变成','下行','促使','激发','加剧','步入','抑制','着力','指引','推动','推进','有望',\
                '放缓','迫使','推向','放宽，期待','操纵','加快','显现','鼓励','提振','助长','遭到','凸显',\
                '拓宽','蔓延','滋生','塑造','整顿','误导','旨在','强化','已经','越来越','不断','逐步','尤其',\
                '最终','就要','依然','几乎','日益','稳步','一度','随后','结果','以便','相继','那么','日趋',\
                '终究','更加','随之','不能不','不得不','不至于','即将','势必','只有','更为','实际上','尽可能']

                '''
                # print(sentences,subsents,subsents[sentens_pos])
                lef_sents_len=len(subsents[sentens_pos].split(tag)[0])
                right_sents_len=len(tag+subsents[sentens_pos].split(tag)[1])
                len_target=len(subsents[sentens_pos])
                current_position,rest_len=get_posion_in_subsent(subsents[sentens_pos],tag)#//得到所在词当前的位置
                if subsents_len==2 and not judeg_subsents_len(subsents,subsents[sentens_pos])  and right_sents_len>=Rest_min_max_len and lef_sents_len>=Rest_min_max_len: #因果都在一句之中
                    yuanyin_sents=subsents[sentens_pos].split(tag)[0]
                    jieguo_sents=tag+subsents[sentens_pos].split(tag)[1]
                    # print(yuanyin_sents,jieguo_sents,tag)
                else:
                    yuanyin_sents=subsents[:sentens_pos]
                    jieguo_sents=subsents[sentens_pos]


    elif len(words)==2:
        tag_1=words[0]
        tag_2=words[1]
        con_words='-'.join(words).strip().replace(' ','')
        double_rule_tags=yg_words+gy_words#二元全部tag
        # print(tag1_sentens_pos,tag2_sentens_pos)
        if con_words in double_rule_tags:
            subsents,tag1_sentens_pos,tag2_sentens_pos,tag1_head,tag2_head=judge_tag_position_in_sentences_2(sentences,words)
            subsents_len=len(subsents)
            if subsents_len!=1 and tag1_sentens_pos!=tag2_sentens_pos:#子句个数>1，tag1和tag2位置不一样
                # print(words)
                # print(yg_words)
                # print(con_words)
                if con_words in yg_words:#由因到果
                    yuanyin_sents=subsents[tag1_sentens_pos]
                    jieguo_sents=subsents[tag2_sentens_pos]
                else:
                    jieguo_sents=subsents[tag1_sentens_pos]
                    yuanyin_sents=subsents[tag2_sentens_pos]
            else:
                # print(sentences)
                # print(tag1_sentens_pos,tag2_sentens_pos)
                # print(words)
                pattern = re.compile(r'(.*)(%s)(.*)(%s)(.*)' % (tag_1, tag_2.strip()))
                result1 = list(pattern.findall(sentences))
                # print(result1)
                lef_sents=result1[0][2]
                right_sents=result1[0][4]
                if con_words in yg_words:#由因到果
                    yuanyin_sents=tag_1+lef_sents
                    jieguo_sents=tag_2+right_sents
                else:
                    jieguo_sents=tag_1+lef_sents
                    yuanyin_sents=tag_2+right_sents
                    # print(yuanyin_sents,jieguo_sents)
        elif con_words in ['起-作用', '是-原因','是-目的','是-结果','是-证明','之?所以-因为', '之?所以-由于', '之?所以-缘于',\
                     '之?所以-因','之?所以-鉴于','之?所以-由',\
                     '之?所以-出于','之?所以-是因为','的目的-是']:#不规则模板
                    if con_words in ['起-作用','是-原因','是-目的','是-结果','是-证明','的目的-是']:
                        subsents,tag1_sentens_pos,tag2_sentens_pos,tag1_head,tag2_head=judge_tag_position_in_sentences_2(sentences,words)
                        # print(tag2_sentens_pos,tag1_sentens_pos)
                        if tag1_sentens_pos==tag2_sentens_pos and tag1_sentens_pos>=1 and len(subsents[tag1_sentens_pos-1])>=4:
                            yuanyin_sents=subsents[:tag1_sentens_pos]
                            jieguo_sents=subsents[tag1_sentens_pos]
                        elif tag1_sentens_pos!=tag2_sentens_pos and tag1_sentens_pos>=1:
                            yuanyin_sents=subsents[tag1_sentens_pos]
                            jieguo_sents=subsents[tag2_sentens_pos]
                        else:
                            pass
                            
                    else:
                        pattern = re.compile(r'(.*)(%s)(.*)(%s)(.*)' % (words[0], words[1]))#
                        result1 = pattern.findall(sentences)
                        yuanyin_part=result1[0][4]
                        jieguo_part=result1[0][2]
                        if len(yuanyin_part.split('，'))>1:
                            yuanyin_sents=yuanyin_part.split('，')[0]
                        else:
                            yuanyin_sents=yuanyin_part
                        if len(jieguo_part.split('，'))>1:
                            jieguo_sents=jieguo_part.split('，')[0]
                        else:
                            jieguo_sents=jieguo_part
                        # print(yuanyin_sents,jieguo_sents)
        else:
            pass

    else:#tag的长度为3,在不同句的位置才能有因果
        tag_1=words[0]
        tag_2=words[1]
        tag_3=words[2]
        con_words='-'.join(words).strip().replace(' ','')
        if con_words in triple_guide_words:
            subsents,tag1_sentens_pos,tag2_sentens_pos,tag3_sentens_pos=judge_tag_position_in_sentences_3(sentences,words)
            if tag1_sentens_pos!=tag2_sentens_pos and tag3_sentens_pos==tag2_sentens_pos:
                yuanyin_sents=subsents[tag1_sentens_pos]
                jieguo_sents=subsents[tag2_sentens_pos]
            elif tag1_sentens_pos==tag2_sentens_pos and tag3_sentens_pos!=tag2_sentens_pos:
                yuanyin_sents=subsents[tag1_sentens_pos]
                jieguo_sents=subsents[tag3_sentens_pos]
            elif tag1_sentens_pos!=tag2_sentens_pos and tag3_sentens_pos!=tag2_sentens_pos:#多组因果
                yuanyin_sents=[subsents[tag1_sentens_pos],subsents[tag2_sentens_pos]]
                jieguo_sents=[subsents[tag2_sentens_pos],subsents[tag3_sentens_pos]]
            else:
                pass
        else:
            pass
    return yuanyin_sents,jieguo_sents,tags

def main(sentence,words):#分裂主控程序
    bool_filter=filter_casual_sentences(sentence,words)
    # print(bool_filter)
    if bool_filter:
        yuanyin_sents=''
        jieguo_sents=''
        tags=words
    else:
        yuanyin_sents,jieguo_sents,tags=split_sentences(sentence,words)
    return yuanyin_sents,jieguo_sents,tags

if __name__ == "__main__":
    path=r'E:/因果抽取_1/Causal_event/data/causality_sentences.txt'
    with codecs.open(path,encoding='utf-8-sig') as fr:
        sentence_lines=fr.readlines()
    all_split_sentences_tags=pd.DataFrame()
    # print(sentence_lines)
    Reasons=[]
    Results=[]
    Tags=[]
    for line in sentence_lines:
        # print(line)
        example_sentence=line.split('  ')[0]#因果句
        example_words=line.split('  ')[1].replace('\n','').replace("'",'').split(',')#引导词
        yuanyin_sents,jieguo_sents,words=main(example_sentence,example_words)
        if len(yuanyin_sents)>=1 and len(jieguo_sents)>=1:
            Reasons.append(yuanyin_sents)
            Results.append(jieguo_sents)
            Tags.append(words)
        else:
            # print(line,yuanyin_sents,jieguo_sents)
            pass

    all_split_sentences_tags['yuanyin_part']=Reasons
    all_split_sentences_tags['jieguo_part']=Results
    all_split_sentences_tags['tags']=Tags
    all_split_sentences_tags.to_csv('E:/因果抽取_1/Causal_event/data/all_split_sentences.csv',encoding='utf-8')

            


            
        












