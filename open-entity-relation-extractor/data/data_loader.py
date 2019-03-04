# -*- coding: utf-8 -*-
'''
Created on 2019年03月04日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pymysql
import datetime
import os
import json
# 打开数据库连接


def fetch_data(path_log='./data/time.txt', force_all=False):
    sql = "select news.id, news.content from news where news.category_id in (select category.id from category where" \
          " category.category_name in ('财经', '财经新闻'))"
    if not force_all:
        if not os.path.exists(path_log):
            pass
        else:
            with open(path_log, 'r') as f:
                sql = "select news.id, news.content from news" \
                      " where news.category_id in (select category.id from category where" \
                      " category.category_name in ('财经', '财经新闻')) and news.insert_time > '" + f.read() + "'"




    db = pymysql.connect("10.214.193.166", "root", "root", "mmgradio")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)

    # 使用 fetchone() 方法获取单条数据.
    data = [dict([('id', d[0]), ('content', d[1])]) for d in cursor.fetchall()]

    # print("Database version : %s " % data)

    # 关闭数据库连接
    db.close()

    return data


def db_to_local():
    sql = "select news.id, news.content from news where news.category_id in (select category.id from category where" \
          " category.category_name in ('财经', '财经新闻')) limit 25"
    db = pymysql.connect("10.214.193.166", "root", "root", "mmgradio")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)

    # 使用 fetchone() 方法获取单条数据.
    data = [dict([('id', d[0]), ('content', d[1])]) for d in cursor.fetchall()]

    # print("Database version : %s " % data)

    # 关闭数据库连接
    db.close()

    with open('example.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


def fetch_data_from_file():
    with open('example.json', 'r', encoding='utf8') as f:
        ret = json.load(f)
    return ret


def update_log(path_log='./data/time.txt'):
    with open(path_log, 'w') as f:
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(t)


if __name__ == '__main__':
    # db_to_local()
    print(fetch_data_from_file())