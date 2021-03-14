# -*- encoding: utf-8 -*-
"""
@Author             :  Hao Shen
@Last Modified by   :  Hao Shen
@Last Modified time :  2021/03/14 01:14:14
@Email              :  shenhao0223sh@gamil.com
@Describe           :  None
"""

# here put the import lib
import json
import pymongo
import os

# filename = "ccpc_valid_v1.0.json"
POETRY_DIRECTORY = './raw_poetry_data/'


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
        for data in f.readlines():
            dict_obj = json.loads(data.strip())
            poem_content = dict_obj['content'].strip().replace("|", ",")
            dict_obj['content'] = poem_content
            del dict_obj["keywords"]
            collection.insert_one(dict_obj)
        print("Success insert data: ", filename)


def main():
    collection = connect_mongodb(db_name="poetry", collection_name="ccpc")
    print("Save to mongodb .....")
    # map返回的是迭代器，迭代器是惰性加载，不遍历不计算，自然看不到输出
    if list(map(save_to_mongodb, os.listdir(POETRY_DIRECTORY),
                [collection for i in range(len(os.listdir(POETRY_DIRECTORY)))])):
        print("Successfully save to mongodb")


if __name__ == "__main__":
    main()
