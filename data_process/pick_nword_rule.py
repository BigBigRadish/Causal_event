# -*- coding: utf-8 -*-
'''
Created on 2019年10月16日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#
import pandas as pd
import codecs
n_path='../data/n_df_fq_001.csv'#名词源文件
v_path='../data/v_df_fq_001.csv'#动词源文件
d_path='../data/d_df_fq_001.csv'#动词源文件
def generate_1vn(path,other_rule_1_words_path,other_rule_2_words_path,other_rule_3_words_path):
    word_df=pd.read_csv(path)
    for index,support_wordpair in word_df.iterrows():
        support_wordpair_1=support_wordpair['itemsets'].replace("'",'').replace('[','').replace(']','').split(',')
        if len(support_wordpair_1)==1:
#             print(support_wordpair)
            with codecs.open(other_rule_1_words_path,'a',encoding='utf-8') as fw_1:
                fw_1.write(str(support_wordpair['support'])+','+support_wordpair_1[0]+'\n')
        elif len(support_wordpair_1)==2:
            with codecs.open(other_rule_2_words_path,'a',encoding='utf-8') as fw_2:
                fw_2.write(str(support_wordpair['support'])+','+'-'.join(support_wordpair_1)+'\n')
        else:
            with codecs.open(other_rule_3_words_path,'a',encoding='utf-8') as fw_3:
                fw_3.write(str(support_wordpair['support'])+','+'-'.join(support_wordpair_1)+'\n')
if __name__ == '__main__':
    other_rule_n1_words_path='../data/v_df_o1.csv'
    other_rule_n2_words_path='../data/v_df_o2.csv'
    other_rule_n3_words_path='../data/v_df_o3.csv'
    generate_1vn(v_path,other_rule_n1_words_path,other_rule_n2_words_path,other_rule_n3_words_path)