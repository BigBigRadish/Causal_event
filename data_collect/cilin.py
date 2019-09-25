import codecs
import json

# def parse_cilin(word1,word2):
def generate_dict(line_):
    for word in line_:
        word1=line_.copy()
        word1.remove(word)
        total_dict[word]=word1
def cilin_file_repro(file_):
    with codecs.open(file_,'r',encoding='utf-8') as fr:
        lines=fr.readlines()
    # print(lines)
    for line in lines:
        line_1=line.replace('\r\n','')
        new_line=line_1.split(' ')[1:]
        generate_dict(new_line)
# def single_word(word1,seed_word_list):

if __name__ == "__main__":
    total_dict={}
    file_path='D:\javaWeb开发\javaworkplace\strategic_research\cilin\同义词林.txt'
    # cilin_file_repro(file_path)
    # with open('D:\javaWeb开发\javaworkplace\strategic_research\cilin\cilin.json','w',encoding='utf-8') as fw:
    #         json.dump(total_dict,fw,ensure_ascii=False)
    with open('./cilin.json','r',encoding='utf-8') as fr:
        a=json.load(fr)
    print(a['我'])
     

    