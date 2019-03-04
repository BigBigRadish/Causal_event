# -*- coding: utf-8 -*-
'''
Created on 2019年03月04日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
from parse_util import *
from tqdm import tqdm
import json
from data.data_loader import fetch_data, update_log, fetch_data_from_file
from data.db_util import NeoManager

dictionary = get_dictionary()


# def get_noun_pairs(sentence):
#     length = len(sentence)
#     pairs = []
#     i = 0
#     while i < length:
#         noun1 = []
#         if sentence[i].is_noun():
#             j = i + 1
#             noun1.append(sentence[i])
#             while j < length:
#                 noun2 = []
#                 if sentence[j].is_noun() and sentence[j].word != sentence[i].word:
#                     # pairs.append((sentence[i], sentence[j]))
#                     noun = sentence[j]
#                     noun2.append(noun)
#                     pairs.append([noun1, noun2])
#                     while noun.relation == 'ATT':
#                         noun = noun.head_word
#                         j = noun.id
#                         noun2.append(noun)
#                 j += 1
#             noun = sentence[i]
#             while noun.relation == 'ATT':
#                 noun = noun.head_word
#                 i = noun.id
#                 noun1.append(noun)
#         i += 1
#     return pairs

# To complete the entity with attributes, for example "特朗普"=>"美国总统特朗普"
def get_full_entity(word, flag=True):
    candidates = []
    if flag or word.relation == 'ATT':
        for w in word.tails:
            attr_list = get_full_entity(w, flag=False)
            for attr in attr_list:
                candidates.append(attr + [word])
        if len(candidates) == 0:
            candidates.append([word])
    if flag:
        candidates = [(len(can), can) for can in candidates if check_entity(can)]
        candidates = [can for _, can in sorted(candidates, key=lambda x: x[0], reverse=True)]
        for can in candidates:
            if len(can) == 1:
                return can
            else:
                if not ('公司' in can[1].word and can[0].postag == 'ns'):
                    return can
        return None
    else:
        candidates = [(len(can), can) for can in candidates]
        candidates = [can for _, can in sorted(candidates, key=lambda x: x[0], reverse=True)]
        ret = []
        for can in candidates:
            if len(can) == 1:
                ret.append(can)
            else:
                if not ('公司' in can[1].word and can[0].postag == 'ns'):
                    ret.append(can)
        return ret


# To find candidate entities
def get_entities(sentence):
    entities = []
    for w in sentence:
        if w.is_noun() and w.relation != 'ATT':
            entity = get_full_entity(w)
            if entity:
                entities.append(entity)

    return entities


# def get_entities(sentence):
#     length = len(sentence)
#     entities = []
#     for i in range(length):
#         words = []
#         if sentence[i].postag in ['nh', 'nz', 'ni'] and sentence[i].is_noun():
#             word = sentence[i]
#             words.append(word)
#             while word.relation == 'ATT':
#                 word = word.head_word
#                 words.append(word)
#             # words = get_attr(sentence[i]).reverse()
#         if check_entity(words):
#             entities.append(words)
#     return entities

# To find entity pairs
def get_entity_pairs(sentence):
    entities = get_entities(sentence)
    pairs = []
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            pairs.append([entities[i], entities[j]])
    return pairs

# To filter entities composed of common nouns like "一个人", we want the entities contain special nouns like "特朗普", "阿里巴巴"
def check_entity(noun_list):
    ret = False
    for n in noun_list:
        ret |= n.is_entity()
    return ret


# (奥巴马)和(特朗普)
def solve_COO(entity, relation='SBV'):
    if entity.relation == relation:
        return entity
    elif entity.relation == 'COO':
        entity = entity.head_word
        if entity.relation == relation:
            return entity
    return None

# 哈德森出身在伦敦。
def SBV_CMP_POB(entity1, entity2):
    ent1 = entity1
    ent2 = entity2
    entity1 = entity1[-1]
    entity2 = entity2[-1]
    if entity1.word == entity2.word:
        return None
    entity2 = solve_COO(entity2, 'POB')
    if entity2 is not None and entity2.relation == 'POB' and entity2.head_word.relation == 'CMP':
        if entity2.head_word.head_word.relation == 'HED':
            entity1 = solve_COO(entity1)
            if entity1 is not None and entity1.relation == 'SBV' and entity1.head_id == entity2.head_word.head_id:
                return ent1, [entity2.head_word.head_word, entity2.head_word], ent2
    else:
        return False

# 乔布斯在斯坦福大学演讲。
def SBV_ADV_POB(entity1, entity2, sentence):
    ent1 = entity1
    ent2 = entity2
    entity1 = entity1[-1]
    entity2 = entity2[-1]
    if entity1.word == entity2.word:
        return None
    entity2 = solve_COO(entity2, 'POB')
    if entity2 is not None and entity2.relation == 'POB' and entity2.head_word.relation == 'ADV':
        if entity2.head_word.head_word.relation == 'HED':
            entity1 = solve_COO(entity1)
            if entity1 is not None and entity1.relation == 'SBV' and entity1.head_id == entity2.head_word.head_id:
                relation = [entity2.head_word.head_word]
                for i in range(entity2.id + 1, len(sentence)):
                    w = sentence[i]
                    if w.relation == 'VOB' and w.head_id == entity2.head_word.head_id:
                        relation.append(w)
                return ent1, relation, ent2
    else:
        return False


# 特朗普是美国总统。
def SBV_VOB(entity1, entity2):
    ent1 = entity1
    ent2 = entity2
    entity1 = entity1[-1]
    entity2 = entity2[-1]
    if entity1.word == entity2.word:
        return None
    entity2 = solve_COO(entity2, 'VOB')
    if entity2 is not None and entity2.relation == 'VOB':
        if entity2.head_word.relation == 'HED':
            entity1 = solve_COO(entity1)
            if entity1 is not None and entity1.relation == 'SBV' and entity1.head_id == entity2.head_id:
                return ent1, [entity2.head_word], ent2
    else:
        return False


# 孟晚舟被拘留。
def FOB_ADV_POB(entity1, entity2):
    ent1 = entity1
    ent2 = entity2
    entity1 = entity1[-1]
    entity2 = entity2[-1]
    if entity1.word == entity2.word:
        return None
    entity2 = solve_COO(entity2, 'POB')
    if entity2 is not None and entity2.relation == 'POB':
        if entity2.head_word.head_word.relation == 'HED':
            entity1 = solve_COO(entity1, 'FOB')
            if entity1 is not None and entity1.relation == 'FOB' and entity1.head_id == entity2.head_word.head_id:
                return ent2, [entity2.head_word.head_word], ent1
        else:
            return False


extra_info = []


def process_person(ent):
    j = None
    name = None
    is_person = False
    flag = False
    k = None
    for i, e in enumerate(ent):
        if e.postag in ['nz', 'j', 'ns', 'ni'] and not is_person:
            flag = True
        if is_person and not ('先生' in e.word or '女士' in e.word):
            j = i
            break
        if e.postag == 'nh':
            is_person = True
            name = [e]
            k = i
    if name is not None:
        if flag:
            extra_info.append({
                'triplet': {'entity1': [name[0].word], 'entity2': [e.word for e in ent[:k]],
                            'relation': [''], 'type1': 'person', 'type2': 'identity'},
                'type': 'EXTRA',
                'sentence': ''.join([e.word for e in ent])

            })
        prop = ent[j:] if j is not None else []
        return {'name': name, 'prop': prop, 'type': 'person'}
    return None


def process_company(ent):
    j = None
    name = None
    for i, e in enumerate(ent):
        if '公司' in e.word and e.word in dictionary['ni']:
            j = i + 1
            name = [e]
    if name is not None:
        prop = ent[j:]
        return {'name': name, 'prop': prop, 'type': 'company'}
    return None


def process_organization(ent):
    j = None
    name = None
    tp = None
    for i, e in enumerate(ent):
        if e.word in dictionary['ni']:
            tp = 'ni'
            j = i + 1
            name = [e]
        elif e.word in dictionary['j']:
            tp = 'j'
            j = i + 1
            name = [e]
    if name is not None:
        prop = ent[j:]
        # if len(prop) > 0:
        #     prop = [WordUnit(-1, '（', '', '', '', '')] + prop + [WordUnit(-1, '）', '', '', '', '')]
        tp = 'organization' if tp == 'ni' else 'abbreviation'
        return {'name': name, 'prop': prop, 'type': tp}
    return None


def process_place(ent):
    for i, e in enumerate(ent):
        if e.postag != 'ns':
            return None
    return {'name': ent, 'prop': [], 'type': 'place'}


def build_triplet(ent1, relation, ent2):
    prop1, prop2 = [], []
    type1, type2 = 'unkown', 'unkown'
    # ent1 = [e.word for e in ent1]

    ent_processed = process_person(ent1) or process_company(ent1) or process_organization(ent1) or process_place(ent1)
    if ent_processed is not None:
        ent1 = ent_processed['name']
        prop1 += ent_processed['prop']
        type1 = ent_processed['type']

    ent_processed = process_person(ent2) or process_company(ent2) or process_organization(ent2) or process_place(ent2)
    if ent_processed is not None:
        ent2 = ent_processed['name']
        prop2 += ent_processed['prop']
        type2 = ent_processed['type']

    ent1 = [e.word for e in ent1 if e.postag != 'm']
    ent2 = [e.word for e in ent2 if e.postag != 'm']
    prop1 = ([r.word for r in prop1]) if len(prop1) > 0 else []
    prop2 = ([r.word for r in prop2]) if len(prop2) > 0 else []
    relation = prop1 + [r.word for r in relation] + prop2

    # if relation[0] == '为':
    #     relation = relation[1:]
    return ent1, relation, ent2, type1, type2


def extract(data, parse_util):

    output = []
    i = data[0]
    news = data[1]
    # news_error = [1729]
    news_error = []
    if i in news_error:
        return []

    text = parse_util.parse(news['content'])
    for sentence in text:
        pairs = get_entity_pairs(sentence)
        for p in pairs:
            temp = SBV_ADV_POB(p[0], p[1], sentence)
            if temp:
                output.append({
                    'sentence': str(sentence),
                    'triplet': dict(zip(['entity1', 'relation', 'entity2', 'type1', 'type2'], build_triplet(*temp))),
                    'type': 'SBV_ADV_POB'
                })
                # print('SBV_ADV_POB')
                # print(build_triplet(*temp))
            temp = SBV_VOB(p[0], p[1])
            if temp:
                # print('SBV_VOB')
                # print(build_triplet(*temp))
                output.append({
                    'sentence': str(sentence),
                    'triplet': dict(zip(['entity1', 'relation', 'entity2', 'type1', 'type2'], build_triplet(*temp))),
                    'type': 'SBV_VOB'
                })
            temp = SBV_CMP_POB(p[0], p[1])
            if temp:
                # print('SBV_CMP_POB')
                # print(build_triplet(*temp))
                output.append({
                    'sentence': str(sentence),
                    'triplet': dict(zip(['entity1', 'relation', 'entity2', 'type1', 'type2'], build_triplet(*temp))),
                    'type': 'SBV_CMP_POB'
                })
            temp = FOB_ADV_POB(*p)
            if temp:
                output.append({
                    'sentence': str(sentence),
                    'triplet': dict(zip(['entity1', 'relation', 'entity2', 'type1', 'type2'], build_triplet(*temp))),
                    'type': 'FOB_ADV_POB'
                })
    return output


def extract_all(data):
    parse_util = ParseUtil()
    output = []
    data = [(i, news) for i, news in zip(range(len(data)), data)]
    for d in tqdm(data):
        output += extract(d, parse_util)
    return output


def test():
    data = fetch_data_from_file()
    data = extract_all(data) + extra_info
    db_manager = NeoManager()
    db_manager.clear()
    db_manager.write2db(data)


if __name__ == '__main__':
    test()
    # data = fetch_data(force_all=True)
    # data = extract_all(data) + extra_info
    # db_manager = NeoManager()
    # db_manager.clear()
    # db_manager.write2db(data)
    # update_log()







