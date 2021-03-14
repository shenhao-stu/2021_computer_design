# -*- coding:utf-8 -*-
# -------------------------------
# @Author : shenhao-stu
# @Email : 56550322@163.com
# -------------------------------
# @File : mongodb_server.py
# @Time : 2021-03-14 16:24
# -------------------------------
from flask import Flask, Response, request
from flask_cors import CORS
import pymongo
import re
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)


def connect_mongodb(db_name, collection_name):
    # connect MongoDB
    client = pymongo.MongoClient(host='localhost', port=27017)
    # select test db
    db = client[db_name]
    # select table/collection
    collection = db[collection_name]
    return collection


def search_data_from_mongodb(collection):
    # find_one() / find()
    result = collection.find_one({'age': {'$gt': 20}})
    results = collection.find({'gender': 'male'})
    count = results.count()
    for result in results:
        print(result)


@app.route('/ccpc', methods=['GET'])
def query_ccpc():
    # initialize variables
    author, content, title = '' if not request.args.get('author') else request.args.get(
        'author'), '' if not request.args.get('content') else request.args.get('content'), '' if not request.args.get(
        'title') else request.args.get('title')
    res = dict()
    print(f"author:{author},content:{content},title:{title}")
    # query sentences
    condition = {'author': re.compile(author), 'content': re.compile(
        content), 'title': re.compile(title)}
    # mongodb connect
    collection = connect_mongodb(db_name="poetry", collection_name="ccpc")
    results = collection.find(condition)
    num_count = results.count()
    index = 0
    for result in results:
        del result['_id']
        res[f"{index}"] = result
        index += 1
    # return response
    response = Response(json.dumps({'msg': 'success', 'state': 'success', 'result': res, 'count': num_count},
                                   ensure_ascii=False).encode('utf-8'), mimetype="application/json")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host='localhost', debug=True)
