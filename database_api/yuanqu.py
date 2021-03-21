# -*- coding:utf-8 -*-
# -------------------------------
# @Author : shenhao-stu
# @Email : 56550322@163.com
# -------------------------------
# @File : yuanqu.py.py
# @Time : 2021-03-15 20:16
# -------------------------------

import json
import pymongo
import os
import re

POETRY_DIRECTORY = './other_poetry/yuanqu'


def connect_mongodb(db_name, collection_name):
    # connect MongoDB
    client = pymongo.MongoClient(host='localhost', port=27017)
    # select test db
    db = client[db_name]
    # select table/collection
    collection = db[collection_name]
    return collection


def save_to_mongodb(filename, collection):
    file_path = os.path.join(POETRY_DIRECTORY, filename)
    # output_path = os.path.join('./poetry_data/', filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        poetry_data = json.loads(f.read().strip())
        for dict_obj in poetry_data:
            # poem_content = dict_obj['paragraphs']
            # modified_str = ""
            # for line in poem_content:
            #     modified_str += line.strip()
            # dict_obj['content'] = modified_str.strip()
            # match dynasty
            dict_obj['content'] = dict_obj['paragraphs']
            if re.search('.*?yuan.*?', filename):
                dict_obj['dynasty'] = 'Yuan'
            if "id" in dict_obj.keys():
                del dict_obj["id"]
            if "paragraphs" in dict_obj.keys():
                del dict_obj["paragraphs"]
            if "tags" in dict_obj.keys():
                del dict_obj["tags"]
            collection.insert_one(dict_obj)
        print("Success insert data: ", filename)


def main():
    collection = connect_mongodb(
        db_name="poetry", collection_name="yuan")
    print("Save to mongodb .....")
    # map返回的是迭代器，迭代器是惰性加载，不遍历不计算，自然看不到输出
    if list(map(save_to_mongodb, os.listdir(POETRY_DIRECTORY),
                [collection for i in range(len(os.listdir(POETRY_DIRECTORY)))])):
        print("Successfully save to mongodb")


if __name__ == "__main__":
    main()
