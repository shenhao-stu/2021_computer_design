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


@app.route('/style_trans', methods=['POST'])
def style_trans():
    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/style_trans"
    if 'file' not in request.files:
        return jsonify({'msg': 'No file part', 'state': 'failure'})
    f = request.files['file']
    img = base64.b64encode(bytearray(f.read()))
    opt = request.form['opt']
    # params = {"image": img, "option": "mononoke"}
    params = {"image": img, "option": opt}
    access_token = ""
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        res = response.json()['image']
        res_img = base64.b64decode(res)
        with open(image_filename, 'wb') as img_obj:
            img_obj.write(res_img)
        response = Response(json.dumps({'msg': 'success', 'state': 'success', 'result': res},
                                       ensure_ascii=False).encode('utf-8'), mimetype="application/json")
        return response


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True)
