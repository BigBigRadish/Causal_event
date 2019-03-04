# -*- coding: utf-8 -*-
'''
Created on 2019年03月04日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
from pyltp import Postagger
from pyltp import Segmentor
import os
from tqdm import tqdm
LTP_DATA_DIR = '/Users/agnostic/NLP/ltp_data'
# LTP_DATA_DIR = '/home/agnostic/dataset/ltp_data'
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')

path_lexicon = './lexicon'
path_company = '/Users/agnostic/NLP/Company-Names-Corpus/Company-Names-Corpus（480W）.txt'
path_short = '/Users/agnostic/NLP/Company-Names-Corpus/Company-Shorter-Form.txt'
path_org = '/Users/agnostic/NLP/Company-Names-Corpus/Organization-Names-Corpus（110W）.txt'
path_name_cn = '/Users/agnostic/NLP/Chinese-Names-Corpus/Chinese_Names_Corpus（120W）.txt'
path_name_en_cn = '/Users/agnostic/NLP/Chinese-Names-Corpus/English_Cn_Name_Corpus（48W）.txt'

comany_names = {'nz', 'nh', 'j', 'ni'}



def check_company(name, segmentor, postagger):
    words = segmentor.segment(name.strip())
    tags = postagger.postag(words)
    for t in tags:
        if t in comany_names:
            return True
        return False

def read(path=path_company, postag='ni', segmentor=None, postagger=None):
    with open(path, 'r', encoding='utf8') as f:
        [f.readline() for _ in range(3)]
        lines = f.readlines()
    if segmentor is not None and postagger is not None:
        return [name.strip() + ' ' + pos + '\n'
                for name, pos in tqdm(zip(lines, [postag] * len(lines))) if check_company(name, segmentor, postagger)]
    return [name.strip() + ' ' + pos + '\n' for name, pos in zip(lines, [postag] * len(lines))]


def write(lines, path=path_lexicon):
    with open(path, 'w+', encoding='utf8') as f:
        f.writelines(lines)


if __name__ == '__main__':
    postagger = Postagger()
    segmentor = Segmentor()
    segmentor.load(cws_model_path)
    postagger.load(pos_model_path)
    lines = read(segmentor=segmentor, postagger=postagger)
    lines += read(path_short, 'j')
    lines += read(path_org)
    lines += read(path_name_cn, 'nh')
    lines += read(path_name_en_cn, 'nh')
    write(lines)
    postagger.release()
    segmentor.release()