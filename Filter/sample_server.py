# -*- coding: utf-8 -*-
# @Author: Hao Shen
# @Last Modified by:   Hao Shen
# @Last Modified time: 2021-02-28 20:37:45
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import base64
import requests
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

image_filename = 'res_img.jpg'


@app.route('/filter', methods=['POST'])
def style_trans():
    request_url = "https://api-cn.faceplusplus.com/facepp/v2/beautify"
    if 'file' not in request.files:
        return jsonify({'msg': 'No file part', 'state': 'failure'})
    f = request.files['file']
    img = base64.b64encode(bytearray(f.read()))
    opt = request.form['opt']
    api_key = ""
    api_secret = ""
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {"api_key": api_key, "api_secret": api_secret, "image_base64": img, "filter_type": opt}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        res = response.json()['result']
        res_img = base64.b64decode(res)
        with open(image_filename, 'wb') as img_obj:
            img_obj.write(res_img)  
        response = Response(json.dumps({'msg': 'success', 'state': 'success', 'result': res},
                                       ensure_ascii=False).encode('utf-8'), mimetype="application/json")
        return response


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=5500, debug=True)
