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

POETRY_DIRECTORY = './simplify_poetry/1'
ANOTHER_POETRY_DIRECTORY = './simplify_poetry/2'


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
            if "paragraphs" in dict_obj.keys():
                dict_obj['content'] = dict_obj["paragraphs"]
                del dict_obj["paragraphs"]
            collection.insert_one(dict_obj)
        print("Success insert data: ", filename)


def another_save_to_mongodb(filename, collection):
    file_path = os.path.join(ANOTHER_POETRY_DIRECTORY, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        poetry_data = json.loads(f.read().strip())
        for type_obj in poetry_data['content']:
            for dict_obj in type_obj['content']:
                dict_obj['type'] = type_obj['type']
                if filename == 'qianjiashi.json':
                    author = dict_obj['author']
                    if re.search(
                            '.*[（](.*?)[）].*', author):
                        dict_obj['author'] = re.sub(
                            '.*?[（](.*?)[）].*?', "", author).strip()
                        dict_obj['dynasty'] = re.search(
                            '.*[（](.*?)[）].*', author).group(1)
                    else:
                        dict_obj['dynasty'] = '未知'
                if "paragraphs" in dict_obj.keys():
                    dict_obj['content'] = dict_obj["paragraphs"]
                    del dict_obj["paragraphs"]
                collection.insert_one(dict_obj)
        print("Success insert data: ", filename)


def main():
    print("Save to mongodb .....")
    # map返回的是迭代器，迭代器是惰性加载，不遍历不计算，自然看不到输出
    for filename in os.listdir(ANOTHER_POETRY_DIRECTORY):
        collection_name = str(filename.replace('.json', '').strip())
        print(f"collection_name:{collection_name}")
        collection = connect_mongodb(
            db_name="poetry", collection_name=collection_name)
        another_save_to_mongodb(filename, collection)
    for filename in os.listdir(POETRY_DIRECTORY):
        collection_name = str(filename.replace('.json', '').strip())
        print(f"collection_name:{collection_name}")
        collection = connect_mongodb(
            db_name="poetry", collection_name=collection_name)
        save_to_mongodb(filename, collection)
    print("Successfully save to mongodb")


if __name__ == "__main__":
    main()
