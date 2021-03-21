# -*- encoding: utf-8 -*-
"""
@Author             :  Hao Shen 
@Last Modified by   :  Hao Shen
@Last Modified time :  2021/03/15 01:48:13
@Email              :  shenhao0223sh@gamil.com
@Describe           :  None
"""

# here put the import lib

import json
import pymongo
import os
import re

POETRY_DIRECTORY = './poetry/'


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
            poem_content = dict_obj['paragraphs']
            # modified_str = ""
            # for line in poem_content:
            #     modified_str += line.strip().replace("，", " ").replace("。", " ")
            #     modified_str += line.strip()
            # dict_obj['content'] = modified_str.strip().replace(" ", ",")
            # dict_obj['content'] = modified_str.strip()
            dict_obj['content'] = poem_content
            if re.search('.*?song.*?', filename):
                dict_obj['dynasty'] = 'Song'
            else:
                dict_obj['dynasty'] = 'Tang'
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
        db_name="poetry", collection_name="tangsongyuan")
    print("Save to mongodb .....")
    # map返回的是迭代器，迭代器是惰性加载，不遍历不计算，自然看不到输出
    if list(map(save_to_mongodb, os.listdir(POETRY_DIRECTORY),
                [collection for i in range(len(os.listdir(POETRY_DIRECTORY)))])):
        print("Successfully save to mongodb")


if __name__ == "__main__":
    main()
