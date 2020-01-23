# -*- coding: utf-8 -*-
'''
Created on 2019年12月03日 下午5:09:16
Zhukun Luo
Jiangxi University of Finance and Economics
'''

from flask import Flask , render_template, request, session
import datetime
import os
from pymongo import MongoClient
from bson import ObjectId
import json
import hashlib
import random
import pandas as pd

host="0.0.0.0"
port=9999
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
from pyltp import SentenceSplitter
LTP_DIR =r'D:\LTP\MODEL\ltp_data'  # ltp模型目录的路径
segmentor = Segmentor()
segmentor.load(os.path.join(LTP_DIR, "cws.model"))# 分词模型路径，模型名称为`cws.model`
postagger = Postagger()
postagger.load(os.path.join(LTP_DIR, "pos.model"))# 词性标注模型路径，模型名称为`pos.model`
 
mongo_con=MongoClient('52.80.213.27', 8888)
db=mongo_con.Causal_event

user_collection=db.Causal_sentence_user
sentences_collection=db.Causal_sentences

app = Flask(__name__,static_folder='download_cache', static_url_path='/download_cache/')

app.secret_key = os.urandom(24)

import re
def cut_sent(para):
    para = re.sub(u'([。！？\?])([^”’])', r"\1\n\2", para)  #单字符断句符
    para = re.sub(u'(\.{6})([^”’])', r"\1\n\2", para)  #英文省略号
    para = re.sub(u'(\…{2})([^”’])', r"\1\n\2", para)  #中文省略号
    para = re.sub(u'([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    #如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  #段尾如果有多余的\n就去掉它
    #很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        # print(session.values())
        uname = session['username']
        if request.form['click'] == '登陆':
            return render_template("index.html")
        else:
            user_collection.insert({'username':uname,'createTime':datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")})
            return render_template("index.html")
       

@app.route('/post', methods=['POST','GET'])
def post():#登陆主页

    f = request.files['file']
    input_text = request.form['input_txt'].encode("utf-8-sig")

    filename = f.filename
    uname = session['username']

    if request.form['click'] == '上传文件':

        #record user ip , date, user_name 
        if filename:
            curr_time = datetime.datetime.now()
            if '.txt' in filename:
                content=f.read().decode(encoding="utf-8-sig")
                sentences=[sentence for sentence in SentenceSplitter.split(content) if sentence]
            # Id=uni_id()
                for i in sentences:
                    sentences_collection.insert({'username':uname,'filename':filename.replace('.txt',''),'sentence':i,'uploadTime':curr_time,'casualtag':'0','eventtag':'0','cflag':'0','eflag':'0'})

                return render_template("upload_succeed.html",suc_message='upload successful')
            else:
                err_message='text format not right!'
                return render_template("upload_error.html",err_message=err_message)
        else:
            curr_time = datetime.datetime.now()
            content=input_text
            sentences=[sentence for sentence in SentenceSplitter.split(content) if sentence]
            for i in sentences:
                sentences_collection.insert({'username':uname,'filename':'输入上传','sentence':i,'uploadTime':curr_time,'casualtag':'0','eventtag':'0','cflag':'0','eflag':'0'})

            return render_template("upload_succeed.html",suc_message='upload successful')

@app.route('/ctag', methods=['GET','POST'])#获取全部已标注因果句文本
def causaltag():
    query_cond={ "casualtag": '1' ,'username':session['username']}
    tag_sentences=list(sentences_collection.find(query_cond,{ "_id": 1,"filename": 1, "sentence": 1 }))#结果集转list
    return render_template("ctag.html", Item=tag_sentences)


@app.route('/cuntag', methods=['GET','POST'])#获取全部未标注因果句文本
def causaluntag():
    query_cond={ 'username':session['username'],'cflag' :'0'}
    untag_sentences=list(sentences_collection.find(query_cond,{ "_id": 1,"filename": 1, "sentence": 1 }))#结果集转list
    print(len(untag_sentences))
    return render_template("cuntag.html", Item=untag_sentences[:25])

@app.route('/saveCtag', methods=['GET','POST'])#存储已标注因果句子
def saveCtag():
    for i,j in request.form.items():#遍历id和编号
        myquery = { "_id": ObjectId(i) }
        newvalues = { "$set": { "casualtag": str(j) ,'cflag':'1'} }
        sentences_collection.update_one(myquery, newvalues)
    query_cond={ "cflag": '0' }
    untag_sentences=list(sentences_collection.find(query_cond,{ "_id": 1,"filename": 1, "sentence": 1 }))#结果集转list
    return render_template("cuntag.html", Item=untag_sentences[:25])#存储之后重新加载

@app.route('/downloadTag', methods=['GET','POST'])#下载已标注句子
def downloadTag():
    query_cond={ 'username':session['username'],'cflag' :'1'}#标志位置1
    untag_sentences=list(sentences_collection.find(query_cond,{ "_id": 0 }))#结果集转list
    data = pd.DataFrame(untag_sentences)
    data.to_csv('./causal_recognize_and_event_tag_sys/download_cache/casualTag.csv',encoding='utf-8-sig')
    return render_template("downsuccess.html")#下载成功页

@app.route('/downloadCasual', methods=['GET','POST'])#下载已标注因果句子
def downloadCasual():
    query_cond={ 'username':session['username'],'cflag' :'1','casualtag':'1'}#标志位置1,因果句置1
    untag_sentences=list(sentences_collection.find(query_cond,{ "_id": 0 }))#结果集转list
    data = pd.DataFrame(untag_sentences)
    data.to_csv('./causal_recognize_and_event_tag_sys/download_cache/casualsentence.csv',encoding='utf-8-sig') 
    return render_template("downsuccess.html")#下载成功页

@app.route('/etag', methods=['GET','POST'])#获取全部已标注因果事件文本
def eventtag():

    return render_template("etag.html", Item=Item)

@app.route('/euntag', methods=['GET','POST'])#获取全部未标注因果事件文本
def eventuntag():
    query_cond={ "eventtag": '0' ,'casualtag':'1'}#事件标注置0，因果句标志置1
    untag_sentences=list(sentences_collection.find(query_cond,{ "_id": 1,"filename": 1, "sentence": 1 }))#结果集转list
    # print(untag_sentences)
    return render_template("euntag.html", Item=untag_sentences)

@app.route('/saveEtag', methods=['GET','POST'])#存储已标注因果事件
def saveEtag():
    for i,j in request.form.items():#遍历id和编号
        myquery = { "_id": ObjectId(i) }
        newvalues = { "$set": { "casualtag": str(j) ,'cflag':'1'} }
        x = sentences_collection.update_one(myquery, newvalues)
    query_cond={ "cflag": '0' }
    untag_sentences=list(sentences_collection.find(query_cond,{ "_id": 1,"filename": 1, "sentence": 1 }))#结果集转list
    return render_template("cuntag.html", Item=untag_sentences[:25])#存储之后重新加载



if __name__== '__main__':
    app.run(host = host,port = port, debug = True)

