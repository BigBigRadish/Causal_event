# -*- coding: utf-8 -*-
'''
Created on 2019年03月04日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
from pyltp import SentenceSplitter
import os
from pyltp import Postagger
from pyltp import Parser
from pyltp import Segmentor
import jieba
from pyltp import NamedEntityRecognizer
# LTP_DATA_DIR = '/Users/agnostic/NLP/ltp_data'
LTP_DATA_DIR = '/home/agnostic/dataset/ltp_data'
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')


class Text:
    def __init__(self, text):
        self.__index = -1
        if type(text) is not list:
            raise TypeError
        self.__text = text

    def __getitem__(self, item):
        if type(item) is not int:
            raise TypeError
        if item >= len(self.__text) or item < 0:
            raise IndexError
        return self.__text[item]

    def __len__(self):
        return len(self.__text)

    @property
    def text(self):
        return self.__text

    def __iter__(self):
        return self

    def __next__(self):
        self.__index += 1
        if self.__index >= len(self.__text):
            self.__index = -1
            raise StopIteration
        else:
            return self.__text[self.__index]


class Sentence:
    def __init__(self, word_units):
        self.__index = -1
        if type(word_units) is not list:
            raise TypeError
        self.__word_units = word_units

    def __getitem__(self, item):
        if type(item) is not int:
            raise TypeError
        if item >= len(self.__word_units) or item < 0:
            raise IndexError
        return self.__word_units[item]

    def __len__(self):
        return len(self.__word_units)

    def __iter__(self):
        return self

    def __next__(self):
        self.__index += 1
        if self.__index >= len(self.__word_units):
            self.__index = -1
            raise StopIteration
        else:
            return self.__word_units[self.__index]

    def __str__(self):
        return ''.join([w.word for w in self.__word_units if w.id != 0])


class WordUnit:
    def __init__(self, id=None, word=None, postag=None, nertag=None, relation=None, head_id=None):
        self.__head_word = None
        self.tails = []
        if head_id is None or word is None or id is None or postag is None or relation is None or nertag is None:
            self.__id = 0
            self.__word = '<ROOT>'
            self.__head_id = None
            self.__postag = None
            self.__relation = None
            self.__nertag = None
        else:
            self.__id = id
            self.__word = word
            self.__head_id = head_id
            self.__postag = postag
            self.__relation = relation
            self.__nertag = nertag

    def set_head_word(self, word_unit):
        self.__head_word = word_unit
        word_unit.tails.append(self)

    def is_middle_attr(self):
        if self.postag != 'ATT':
            return False
        for t in self.tails:
            if t.head_id == self.id and t.postag == 'ATT':
                return False
        return True

    @property
    def id(self):
        return self.__id

    @property
    def word(self):
        return self.__word

    @property
    def head_id(self):
        return self.__head_id

    @property
    def postag(self):
        return self.__postag

    @property
    def relation(self):
        return self.__relation

    @property
    def nertag(self):
        return self.__nertag

    @property
    def head_word(self):
        return self.__head_word

    def __str__(self):
        return self.word

    def is_entity(self):
        return False if self.postag is None or self.postag not in ['nh', 'ni', 'ns', 'nz', 'j'] else True

    def is_noun(self):
        return False if self.postag is None or self.postag not in ['nh', 'ni', 'ns', 'nz', 'j', 'n'] else True


class ParseUtil:
    def __init__(self, lexicon_path='./data/lexicon'):
        postagger = Postagger()
        postagger.load_with_lexicon(pos_model_path, lexicon_path)
        parser = Parser()
        parser.load(par_model_path)
        # segmentor = Segmentor()
        # segmentor.load_with_lexicon(cws_model_path, lexicon_path)
        recognizer = NamedEntityRecognizer()
        recognizer.load(ner_model_path)
        self.postagger = postagger
        self.parser = parser
        # self.segmentor = segmentor
        self.recognizer = recognizer
        jieba.load_userdict(lexicon_path)
        jieba.enable_parallel(12)
        # with open(lexicon_path, 'r', encoding='utf8') as f:
        #     for line in f:
        #         jieba.add_word(line.split(' ')[0])

    def __del__(self):
        self.postagger.release()
        self.parser.release()
        # self.segmentor.release()
        self.recognizer.release()

    def parse(self, text):
        sents = SentenceSplitter.split(text)
        sentences = []
        for sent in sents:
            # if len(sent) > 40:
            #     continue
            # words = [w for w in self.segmentor.segment(sent)]
            words = [w for w in jieba.cut(sent)]
            postags = [p for p in self.postagger.postag(words)]
            netags = [n for n in self.recognizer.recognize(words, postags)]
            arcs = [a for a in self.parser.parse(words, postags)]
            word_units = [WordUnit()]
            sentences.append(Sentence(word_units))
            for i, (w, p, n, a) in enumerate(zip(words, postags, netags, arcs)):
                word_unit = WordUnit(i + 1, w, p, n, a.relation, a.head)
                word_units.append(word_unit)

            for i in range(len(word_units)):
                if i != 0:
                    word_unit = word_units[i]
                    word_unit.set_head_word(word_units[word_unit.head_id])
        return Text(sentences)


def get_dictionary(lexicon_path='./data/lexicon'):
    ret = {'j': set(), 'nh': set(), 'ni': set()}
    with open(lexicon_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            word, tag = line.strip().split(' ')
            ret[tag].add(word)
    return ret




if __name__ == '__main__':
    import jieba.posseg as pseg
    postagger = Postagger()
    segmentor = Segmentor()
    segmentor.load(cws_model_path)
    postagger.load(pos_model_path)
    string = "公司总会"
    words = [w for w in segmentor.segment(string)]
    tags = postagger.postag(words)
    res = pseg.cut(string)
    print([(w, t) for w, t in zip(words, tags)])
    print([(w, t) for w, t in res])








