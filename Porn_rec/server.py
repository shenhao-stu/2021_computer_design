import base64
import requests
import json
from flask import Flask, request, Response, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/porn', methods=['POST'])
def porn_rec():
    response = requests.get(
        'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id= &client_secret= ')
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"
    if 'file' not in request.files:
        return jsonify({'msg': 'No file part', 'state': 'failure'})
    f = request.files['file']
    img = base64.b64encode(bytearray(f.read()))
    params = {"image": img}
    access_token = response.json()['access_token']
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        res = response.json()['conclusion']
        response = Response(json.dumps({'msg': 'success', 'state': 'success', 'result': res},
                                       ensure_ascii=False).encode('utf-8'), mimetype="application/json")
        return response
    else:
        return Response(json.dumps({'msg': 'failed', 'state': 'failed', 'result': 'error'},
                                   ensure_ascii=False).encode('utf-8'), mimetype="application/json")
