'''
Created on 2019年9月25日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import json
import codecs
def extend_2_words(word1,word2,cilin_dict):#2个词的模板拓展
#     with codecs.open(file_path,'a',encoding='utf-8') as fw1 :
    rule2_extend.append(word1+'-'+word2)
    if len(cilin_dict[word2])>0:
        
        for extend_i in cilin_dict[word2]:
            if len(extend_i)<2:#单个词太杂
                continue
            else:
                rule2_extend.append(word1+'-'+extend_i)
    if len(cilin_dict[word1])>0:
        for extend_j in cilin_dict[word1]:
            if len(extend_j)<2:
                continue
            else:
                rule2_extend.append(word2+'-'+extend_j)        
def extend_1_word(word,cilin_dict,rule):#1个词的模板拓展
    rule.append(word)
    if len(cilin_dict[word])>0:
        for extend_i in cilin_dict[word]:
            if len(extend_i)<2:#单个字太杂
                continue
            else:
                rule.append(extend_i)   
        
    

if __name__ == "__main__":
    with open('./cilin.json','r',encoding='utf-8') as fr:#加载同义词林词典
        cilin_dict=json.load(fr)
    '''
    由因到果配套式
            因为,从而),(因为,为此),(既[然],所以),(因为,为此),(由于,为此),(只有|除非,才),(由于,以至[于]>,(既[然],却>,
            (如果,那么|则),<由于,从而),<既[然],就),(既[然],因此),(如果,就),(只要,就)(因为,所以), <由于,于是),(因为,因此),
         <由于,故), (因为,以致[于]),(因为,因而),(由于,因此),<因为,于是),(由于,致使),(因为,致使),(由于,以致[于] >
         (因为,故),(因[为],以至[于]>,(由于,所以),(因为,故而),(由于,因而
    '''
    rule2=['因为 从而','因为 为此','既 所以','既然 所以','因为 为此','由于 为此','只有 才','除非 才'\
           ,'由于 以至','既然 却','如果 那么','如果 则','由于 从而','既然 就','既然 如此','如果 就','只要 就'\
           ,'因为 所以','由于 于是','因为 因此','由于 故','因 以至','因为 以致','因为 因而','由于 因此','因为 于是','由于 致使'\
           ,'因为 致使','由于 以致','因为 故','因为 以至于','由于 所以','因为 故而','由于 因而']
    rule2_extend=[]
#     for word_pair in rule2:
#         word1=word_pair.split(' ')[0]
#         word2=word_pair.split(' ')[1]
#         extend_2_words(word1,word2,cilin_dict)
#     rule2_extend_=list(set(rule2_extend))
#     print(len(rule2_extend_))
#     file_name=r'C:\Users\Agnostic\Desktop\cilin\seed_extend\由因到果配套式_1_'+str(len(rule2_extend_))+'.txt'
#     with codecs.open(file_name,'a',encoding='utf-8') as fw1:
#         for word_pair_ in rule2_extend_:
#             fw1.write(word_pair_+',')


    '''
            由因到果居中式明确
            于是,所以,故,致使,以致[于],因此,以至[于],从而,因而
    '''
#     rule3=['于是','所以','故','致使','以致','因此','以至','从而','因而']  
#     rule3_extend=[]
#     for word in rule3:
#         extend_1_word(word,cilin_dict,rule3_extend)
#     rule3_extend_=list(set(rule3_extend))
#     file_name=r'C:\Users\Agnostic\Desktop\cilin\seed_extend\由因到果居中式_'+str(len(rule3_extend_))+'.txt'
#     with codecs.open(file_name,'a',encoding='utf-8') as fw1:
#         for word_pair_ in rule3_extend_:
#             fw1.write(word_pair_+',')

    '''
    4由因到果居中式精确
    '''


#     rule4=['牵动','导向','导致','指引','使','促成','造成','促使','酿成',\
#             '引发','促进','引起','引来','诱发','推进','诱致','推动','招致','致使','滋生','归于',\
#             '使得','引出','带来','触发','渗入','波及','诱使']  
#     rule4_extend=[]
#     for word in rule4:
#         extend_1_word(word,cilin_dict,rule4_extend)
#     rule4_extend_=list(set(rule4_extend))
#     file_name=r'C:\Users\Agnostic\Desktop\cilin\seed_extend\由因到果居中式精确_'+str(len(rule4))+'_'+str(len(rule4_extend_))+'.txt'
#     with codecs.open(file_name,'a',encoding='utf-8') as fw1:
#         for word_pair_ in rule4_extend_:
#             fw1.write(word_pair_+',')

    '''
    5由因到果前端式模糊
    '''
#     rule5=['为了','依据','按照','因','按','依赖','照','比','凭借','由于']  
#     rule5_extend=[]
#     for word in rule5:
#         extend_1_word(word,cilin_dict,rule5_extend)
#     rule5_extend_=list(set(rule5_extend))
#     file_name=r'C:\Users\Agnostic\Desktop\cilin\seed_extend\由因到果前端式模糊_'+str(len(rule5))+'_'+str(len(rule5_extend_))+'.txt'
#     with codecs.open(file_name,'a',encoding='utf-8') as fw1:
#         for word_pair_ in rule5_extend_:
#             fw1.write(word_pair_+',')
    '''
    6由因到果居中式模糊
    '''
    rule6=['为了','依据','按照','因','按','依赖','照','比','凭借','由于']  
    rule6_extend=[]
    for word in rule6:
        extend_1_word(word,cilin_dict,rule6_extend)
    rule6_extend_=list(set(rule6_extend))
    file_name=r'C:\Users\Agnostic\Desktop\cilin\seed_extend\由因到果居中式模糊_'+str(len(rule6))+'_'+str(len(rule6_extend_))+'.txt'
    with codecs.open(file_name,'a',encoding='utf-8') as fw1:
        for word_pair_ in rule6_extend_:
            fw1.write(word_pair_+',')
                    
    
    